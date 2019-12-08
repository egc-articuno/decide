from django.db import models
from django.contrib.postgres.fields import JSONField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.validators import RegexValidator

from base import mods
from base.models import Auth, Key

# ----------- NEW MODELS -------------------------------------------------

class Voting(models.Model):
    name = models.CharField(max_length=200)
    desc = models.TextField(blank=True, null=True)

    start_date = models.DateTimeField(blank=True, null=True)
    end_date = models.DateTimeField(blank=True, null=True)

    pub_key = models.OneToOneField(Key, related_name='voting', blank=True, null=True, on_delete=models.SET_NULL)
    auths = models.ManyToManyField(Auth, related_name='votings')

    tally = JSONField(blank=True, null=True)
    postproc = JSONField(blank=True, null=True)

    def create_pubkey(self):
        if self.pub_key or not self.auths.count():
            return

        auth = self.auths.first()
        data = {
            "voting": self.id,
            "auths": [ {"name": a.name, "url": a.url} for a in self.auths.all() ],
        }
        key = mods.post('mixnet', baseurl=auth.url, json=data)
        pk = Key(p=key["p"], g=key["g"], y=key["y"])
        pk.save()
        self.pub_key = pk
        self.save()

    def get_votes(self, token=''):
        # gettings votes from store
        votes = mods.get('store', params={'voting_id': self.id}, HTTP_AUTHORIZATION='Token ' + token)
        # anon votes
        return [[i['a'], i['b']] for i in votes]

    def tally_votes(self, token=''):
        '''
        The tally is a shuffle and then a decrypt
        '''

        votes = self.get_votes(token)

        auth = self.auths.first()
        shuffle_url = "/shuffle/{}/".format(self.id)
        decrypt_url = "/decrypt/{}/".format(self.id)
        auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

        # first, we do the shuffle
        data = { "msgs": votes }
        response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
                response=True)
        if response.status_code != 200:
            # TODO: manage error
            pass

        # then, we can decrypt that
        data = {"msgs": response.json()}
        response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
                response=True)

        if response.status_code != 200:
            # TODO: manage error
            pass

        self.tally = response.json()
        self.save()

        self.do_postproc()

    def do_postproc(self):
        tally = self.tally
        parties = self.parties.all()
        
        opts = []
        for pty in parties:
            for p in pty.president_candidates.all():
                if isinstance(tally, list):
                    votes = tally.count(p.number)
                else:
                    votes = 0
                opts.append({
                    'option': p.president_candidate,
                    'number': p.number,
                    'votes': votes,
                    'gender': p.gender,
                    'postal_code': p.postal_code,
                    'candidate_type': 'president',
                    'party': pty.name
                })
            for c in pty.congress_candidates.all():
                if isinstance(tally, list):
                    votes = tally.count(c.number)
                else:
                    votes = 0
                opts.append({
                    'option': c.congress_candidate,
                    'number': c.number,
                    'votes': votes,
                    'gender': c.gender,
                    'postal_code': c.postal_code,
                    'candidate_type': 'congress',
                    'party': pty.name
                })

        data = { 'type': 'IDENTITY', 'options': opts }
        print(data)
        postp = mods.post('postproc', json=data)

        self.postproc = postp
        self.save()

    def __str__(self):
        return self.name

class PoliticalParty(models.Model):
    name = models.CharField(max_length=100)
    voting = models.ForeignKey(Voting, related_name='parties', on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class PartyPresidentCandidate(models.Model):
    politicalParty = models.ForeignKey(PoliticalParty, related_name='president_candidates', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(blank=True, null=True)
    president_candidate = models.CharField(max_length=100)
    choices = (
        ('H', 'Hombre'),
        ('M', 'Mujer')
    )
    gender = models.CharField(max_length=1, choices=choices)
    postal_code = models.CharField(max_length=5, validators=[RegexValidator(r'^[0-9]{5}$')])

    def save(self):
        if not self.number:
            self.number = self.politicalParty.president_candidates.count() + 2
        return super().save()

    def __str__(self):
        return '{} ({})'.format(self.president_candidate, self.number)

class PartyCongressCandidate(models.Model):
    politicalParty = models.ForeignKey(PoliticalParty, related_name='congress_candidates', on_delete=models.CASCADE)
    number = models.PositiveIntegerField(blank=True, null=True)
    congress_candidate = models.CharField(max_length=100)
    choices = (
        ('H', 'Hombre'),
        ('M', 'Mujer')
    )
    gender = models.CharField(max_length=1, choices=choices)
    postal_code = models.CharField(max_length=5, validators=[RegexValidator(r'^[0-9]{5}$')])
    
    def save(self):
        if not self.number:
            self.number = self.politicalParty.congress_candidates.count() + 2
        return super().save()

    def __str__(self):
        return '{} ({})'.format(self.congress_candidate, self.number)

# -------------------------------------------------------------------------



# ---------- OLD MODELS -------------------------------------

# class Question(models.Model):
#     desc = models.TextField()

#     def __str__(self):
#         return self.desc


# class QuestionOption(models.Model):
#     question = models.ForeignKey(Question, related_name='options', on_delete=models.CASCADE)
#     number = models.PositiveIntegerField(blank=True, null=True)
#     option = models.TextField()

#     def save(self):
#         if not self.number:
#             self.number = self.question.options.count() + 2
#         return super().save()

#     def __str__(self):
#         return '{} ({})'.format(self.option, self.number)

# class Voting(models.Model):
#     name = models.CharField(max_length=200)
#     desc = models.TextField(blank=True, null=True)
#     question = models.ForeignKey(Question, related_name='voting', on_delete=models.CASCADE)

#     start_date = models.DateTimeField(blank=True, null=True)
#     end_date = models.DateTimeField(blank=True, null=True)

#     pub_key = models.OneToOneField(Key, related_name='voting', blank=True, null=True, on_delete=models.SET_NULL)
#     auths = models.ManyToManyField(Auth, related_name='votings')

#     tally = JSONField(blank=True, null=True)
#     postproc = JSONField(blank=True, null=True)

#     def create_pubkey(self):
#         if self.pub_key or not self.auths.count():
#             return

#         auth = self.auths.first()
#         data = {
#             "voting": self.id,
#             "auths": [ {"name": a.name, "url": a.url} for a in self.auths.all() ],
#         }
#         key = mods.post('mixnet', baseurl=auth.url, json=data)
#         pk = Key(p=key["p"], g=key["g"], y=key["y"])
#         pk.save()
#         self.pub_key = pk
#         self.save()

#     def get_votes(self, token=''):
#         # gettings votes from store
#         votes = mods.get('store', params={'voting_id': self.id}, HTTP_AUTHORIZATION='Token ' + token)
#         # anon votes
#         return [[i['a'], i['b']] for i in votes]

#     def tally_votes(self, token=''):
#         '''
#         The tally is a shuffle and then a decrypt
#         '''

#         votes = self.get_votes(token)

#         auth = self.auths.first()
#         shuffle_url = "/shuffle/{}/".format(self.id)
#         decrypt_url = "/decrypt/{}/".format(self.id)
#         auths = [{"name": a.name, "url": a.url} for a in self.auths.all()]

#         # first, we do the shuffle
#         data = { "msgs": votes }
#         response = mods.post('mixnet', entry_point=shuffle_url, baseurl=auth.url, json=data,
#                 response=True)
#         if response.status_code != 200:
#             # TODO: manage error
#             pass

#         # then, we can decrypt that
#         data = {"msgs": response.json()}
#         response = mods.post('mixnet', entry_point=decrypt_url, baseurl=auth.url, json=data,
#                 response=True)

#         if response.status_code != 200:
#             # TODO: manage error
#             pass

#         self.tally = response.json()
#         self.save()

#         self.do_postproc()

#     def do_postproc(self):
#         tally = self.tally
#         options = self.question.options.all()

#         opts = []
#         for opt in options:
#             if isinstance(tally, list):
#                 votes = tally.count(opt.number)
#             else:
#                 votes = 0
#             opts.append({
#                 'option': opt.option,
#                 'number': opt.number,
#                 'votes': votes
#             })

#         data = { 'type': 'IDENTITY', 'options': opts }
#         postp = mods.post('postproc', json=data)

#         self.postproc = postp
#         self.save()

#     def __str__(self):
#         return self.name

# -----------------------------------------------------------