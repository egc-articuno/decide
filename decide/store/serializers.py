from rest_framework import serializers

from .models import Vote, Cipher


class CipherSerializer(serializers.HyperlinkedModelSerializer):
    a = serializers.IntegerField()
    b = serializers.IntegerField()

    class Meta:
        model = Vote
        fields = ('a', 'b')

class VoteSerializer(serializers.HyperlinkedModelSerializer):
    ciphers = CipherSerializer(many=True)

    class Meta:
        model = Vote
        fields = ('voting_id', 'voter_id', 'ciphers')