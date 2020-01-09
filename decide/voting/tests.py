import random
import itertools
from django.utils import timezone
from django.conf import settings
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework.test import APITestCase

from base import mods
from base.tests import BaseTestCase
from census.models import Census
from mixnet.mixcrypt import ElGamal
from mixnet.mixcrypt import MixCrypt
from mixnet.models import Auth
from voting.models import Voting, PartyCongressCandidate, PartyPresidentCandidate, PoliticalParty


class VotingTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()

    def tearDown(self):
        super().tearDown()

    def encrypt_msg(self, msg, v, bits=settings.KEYBITS):
        aux = v
        pk = aux.pub_key
        p, g, y = (pk.p, pk.g, pk.y)
        k = MixCrypt(bits=bits)
        k.k = ElGamal.construct((p, g, y))
        return k.encrypt(msg)

    def create_voting(self):
        v = Voting(name='Elecciones 2020',blank_vote=1)
        v.save()

        p = PoliticalParty(name='test politicalParty', voting=v)
        p.save()

        i = 2
        while i >=  51: # Save 50 presidents
            opt1 = PartyPresidentCandidate(politicalParty=p, number=i, president_candidate="President " + i, gender='H', postal_code="41410")
            opt1.save()
            i += 1
                        
        while i >=  101: # Save 50 congresses
            opt2 = PartyCongressCandidate(politicalParty=p, number=i, congress_candidate="Congress " + i, gender='M', postal_code="41410")
            opt2.save()
            i += 1
            
        a, _ = Auth.objects.get_or_create(url=settings.BASEURL, defaults={'me': True, 'name': 'test auth'})
        a.save()
        v.auths.add(a)

        res = v

        return res

    def create_voters(self, v):
        for i in range(100):
            u, _ = User.objects.get_or_create(username='testvoter{}'.format(i))
            u.is_active = True
            u.save()
            c = Census(voter_id=u.id, voting_id=v.id)
            c.save()

    def get_or_create_user(self, pk):
        user, _ = User.objects.get_or_create(pk=pk)
        user.username = 'user{}'.format(pk)
        user.set_password('qwerty')
        user.save()
        return user

    def store_votes(self, v):
        voters = list(Census.objects.filter(voting_id=v.id))
        voter = voters.pop()

        clear = {}

        data = {
            'voting': v.id,
            'voter': voter.voter_id,
            'votes': []
        }
        for pty in v.parties.all():
            for p in pty.president_candidates.all():
                clear[p.number] = 0
                # for i in range(random.randint(0, 5)):
                for i in range(1):
                    a, b = self.encrypt_msg(p.number, v)
                    data['votes'].append({'a': a, 'b': b})
                    clear[p.number] += 1
            for c in pty.congress_candidates.all():
                clear[c.number] = 0
                # for i in range(random.randint(0, 5)):
                for i in range(1):
                    a, b = self.encrypt_msg(c.number, v)
                    data['votes'].append({'a': a, 'b': b})
                    clear[c.number] += 1
            user = self.get_or_create_user(voter.voter_id)
            self.login(user=user.username)
            voter = voters.pop()
            mods.post('store', json=data)

        return clear

    def test_complete_voting(self):
        v = self.create_voting()
        v1 = v
        self.create_voters(v1)

        v1.create_pubkey()
        v1.start_date = timezone.now()
        v1.save()

        clear = self.store_votes(v)

        self.login()  # set token
        v1.tally_votes(self.token)

        tally = v1.tally
        tally.sort()
        tally = {k: len(list(x)) for k, x in itertools.groupby(tally)}
        print(tally)

        for pty in v.parties.all():
            for p in pty.president_candidates.all():
                self.assertEqual(tally.get(p.number, 0), clear.get(p.number, 0))
            for c in pty.congress_candidates.all():
                self.assertEqual(tally.get(c.number, 0), clear.get(c.number, 0))

        for q in v.postproc:
            self.assertEqual(tally.get(q["number"], 0), q["votes"])

    def test_create_voting_from_api(self):
        data = {'name': 'Example'}
        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        response = mods.post('voting', params=data, response=True)
        self.assertEqual(response.status_code, 400)

        data = {
            'name': 'Elecciones 2020',
            'desc': 'Vota la partido',
            'blank_vote': 2
        }

        response = self.client.post('/voting/', data, format='json')
        self.assertEqual(response.status_code, 201)

    def test_supdate_voting(self):
        voting = self.create_voting()

        data = {'action': 'start'}
        #response = self.client.post('/voting/{}/'.format(voting.pk), data, format='json')
        #self.assertEqual(response.status_code, 401)

        # login with user no admin
        self.login(user='noadmin')
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 403)

        # login with user admin
        self.login()
        data = {'action': 'bad'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)

        # STATUS VOTING: not started
        for action in ['stop', 'tally']:
            data = {'action': action}
            response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
            self.assertEqual(response.status_code, 400)
            self.assertEqual(response.json(), 'Voting is not started')

        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting started')

        # STATUS VOTING: started
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting is not stopped')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting stopped')

        # STATUS VOTING: stopped
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Voting tallied')

        # STATUS VOTING: tallied
        data = {'action': 'start'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already started')

        data = {'action': 'stop'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already stopped')

        data = {'action': 'tally'}
        response = self.client.put('/voting/{}/'.format(voting.pk), data, format='json')
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json(), 'Voting already tallied')