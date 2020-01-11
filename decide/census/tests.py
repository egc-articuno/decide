import random
from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.test import APIClient

from .models import Census
from base import mods
from base.tests import BaseTestCase


class CensusTestCase(BaseTestCase):

    def setUp(self):
        super().setUp()
        self.census = Census(voting_id=1, voter_id=1)
        self.census.save()

    def tearDown(self):
        super().tearDown()
        self.census = None

    def test_check_vote_permissions(self):
        response = self.client.get('/census/{}/?voter_id={}'.format(1, 2), format='json')
        self.assertEqual(response.status_code, 401)
        self.assertEqual(response.json(), 'Invalid voter')

        response = self.client.get('/census/{}/?voter_id={}'.format(1, 1), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), 'Valid voter')

    def test_list_voting(self):
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.get('/census/?voting_id={}'.format(1), format='json')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {'voters': [1]})

    def test_add_new_voters_conflict(self):
        data = {'voting_id': 1, 'voters': [1]}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 409)

    def test_add_new_voters(self):
        data = {'voting_id': 2, 'voters': [1,2,3,4]}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 401)

        self.login(user='noadmin')
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 403)

        self.login()
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertEqual(len(data.get('voters')), Census.objects.count() - 1)

    def test_destroy_voter(self):
        data = {'voters': [1]}
        response = self.client.delete('/census/{}/'.format(1), data, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertEqual(0, Census.objects.count())

    def test_save_census(self):
        data = {'voting_id': 123, 'voter_id': 123}
        census_before = len(Census.objects.all().values_list('voting_id', flat=True))


        admin = User(email='administrador@gmail.com', password='qwerty')
        admin.is_staff = True
        admin.save()

        self.client.force_login(admin)

        response = self.client.get('/census/saveNewCensus', {'voting_id': 123, 'voter_id': 123})

        census_after = len(Census.objects.all().values_list('voting_id', flat=True))
        self.assertTrue(census_before < census_after)

    def test_add_draft_conflict(self):
        self.login()
        data = {'voting_id': 0, 'voters': [0,0]}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 409)

    def test_draft_to_census(self):
        self.login()
        censusdraft = Census(voting_id=0, voter_id=0)
        votingnuevo = "2"
        voternuevo = "150"
        censusdraft = Census(voting_id=votingnuevo, voter_id=voternuevo)
        censusdraft.save

        data = {'voting_id': censusdraft.voting_id, 'voters': censusdraft.voter_id}
        response = self.client.post('/census/', data, format='json')
        self.assertEqual(response.status_code, 201)
    
    def test_save_census_CP(self):
        data = {'postal_code':11223}
        census_1 = len(Census.objects.all().values_list('voting_id', flat=True))


        admin = User(email='administrador@gmail.com', password='qwerty')
        admin.is_staff = True
        admin.save()

        self.client.force_login(admin)

        response = self.client.get('/census/saveNewCensusCP', {'postal_code':11223})

        census_2 = len(Census.objects.all().values_list('voting_id', flat=True))
        self.assertTrue(census_1 == census_2)
        self.assertEqual(response.status_code, 302)

    def test_add_new_census_CP(self):
        data = {'postal_code': 11223}

        self.login()
        response = self.client.post('/census/addCensusCP', {'postal_code': 11223}, format='json')
        self.assertEqual(response.status_code, 200)

