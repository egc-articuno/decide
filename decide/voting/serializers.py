from rest_framework import serializers

from .models import Voting, PartyPresidentCandidate, PartyCongressCandidate, PoliticalParty
from base.serializers import KeySerializer, AuthSerializer

# ---------------- NEW SERIALIZERS ------------------------------

class PartyPresidentCandidateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PartyPresidentCandidate
        fields = ('number', 'president_candidate', 'gender', 'postal_code')

class PartyCongressCandidateSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = PartyCongressCandidate
        fields = ('number', 'congress_candidate', 'gender', 'postal_code')

class PartySerializer(serializers.HyperlinkedModelSerializer):
    president_candidates = PartyPresidentCandidateSerializer(many=True)
    congress_candidates = PartyCongressCandidateSerializer(many=True)

    class Meta:
        model = PoliticalParty
        fields = ('name', 'president_candidates', 'congress_candidates')

class VotingSerializer(serializers.HyperlinkedModelSerializer):
    parties = PartySerializer(many=True)
    pub_key = KeySerializer()
    auths = AuthSerializer(many=True)

    class Meta:
        model = Voting
        fields = ('id', 'name', 'desc', 'parties', 'start_date',
                  'end_date', 'pub_key', 'auths', 'tally', 'postproc')


class SimpleVotingSerializer(serializers.HyperlinkedModelSerializer):
    party = PartyPresidentCandidateSerializer(many=False)

    class Meta:
        model = Voting
        fields = ('name', 'desc', 'party', 'start_date', 'end_date')

# ---------------------------------------------------------------




# ----------- OLD SERIALIZERS ------------------------------------

# class QuestionOptionSerializer(serializers.HyperlinkedModelSerializer):
#     class Meta:
#         model = QuestionOption
#         fields = ('number', 'option')

# class QuestionSerializer(serializers.HyperlinkedModelSerializer):
#     options = QuestionOptionSerializer(many=True)
#     class Meta:
#         model = Question
#         fields = ('desc', 'options')
#
# class VotingSerializer(serializers.HyperlinkedModelSerializer):
#     question = QuestionSerializer(many=False)
#     pub_key = KeySerializer()
#     auths = AuthSerializer(many=True)

#     class Meta:
#         model = Voting
#         fields = ('id', 'name', 'desc', 'question', 'start_date',
#                   'end_date', 'pub_key', 'auths', 'tally', 'postproc')


# class SimpleVotingSerializer(serializers.HyperlinkedModelSerializer):
#     question = QuestionSerializer(many=False)

#     class Meta:
#         model = Voting
#         fields = ('name', 'desc', 'question', 'start_date', 'end_date')

# ------------------------------------------------------------------------