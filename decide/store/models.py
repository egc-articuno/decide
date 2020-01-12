from django.db import models
from base.models import BigBigField



class Vote(models.Model):
    voting_id = models.PositiveIntegerField()
    voter_id = models.PositiveIntegerField()

    voted = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {}'.format(self.voting_id, self.voter_id)

# -------------------- NEW Model ---------
class Cipher(models.Model):
    a = BigBigField()
    b = BigBigField()
    vote = models.ForeignKey(Vote, related_name='ciphers', on_delete=models.CASCADE)

    def __str__(self):
        return '{}: {}'.format(self.a, self.b)
# ----------------------------------------