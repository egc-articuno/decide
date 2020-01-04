from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from django.shortcuts import redirect, render
from rest_framework.status import (
        HTTP_201_CREATED as ST_201,
        HTTP_204_NO_CONTENT as ST_204,
        HTTP_400_BAD_REQUEST as ST_400,
        HTTP_401_UNAUTHORIZED as ST_401,
        HTTP_409_CONFLICT as ST_409
)

from base.perms import UserIsStaff
from .models import Census
from voting.models import Voting
from census.serializer import CensusSerializer


class CensusCreate(generics.ListCreateAPIView):
    permission_classes = (UserIsStaff,)

    def create(self, request, *args, **kwargs):
        voting_id = request.data.get('voting_id')
        voters = request.data.get('voters')
        try:
            for voter in voters:
                census = Census(voting_id=voting_id, voter_id=voter)
                census.save()
        except IntegrityError:
            return Response('Error try to create census', status=ST_409)
        return Response('Census created', status=ST_201)

    def list(self, request, *args, **kwargs):
        voting_id = request.GET.get('voting_id')
        voters = Census.objects.filter(voting_id=voting_id).values_list('voter_id', flat=True)
        return Response({'voters': voters})


class CensusDetail(generics.RetrieveDestroyAPIView):

    def destroy(self, request, voting_id, *args, **kwargs):
        voters = request.data.get('voters')
        census = Census.objects.filter(voting_id=voting_id, voter_id__in=voters)
        census.delete()
        return Response('Voters deleted from census', status=ST_204)

    def retrieve(self, request, voting_id, *args, **kwargs):
        voter = request.GET.get('voter_id')
        try:
            Census.objects.get(voting_id=voting_id, voter_id=voter)
        except ObjectDoesNotExist:
            return Response('Invalid voter', status=ST_401)
        return Response('Valid voter')



def list_census(request):

    census = Census.objects.all()
    votings = Voting.objects.all()
    return render(request,"main_index.html",{'census': census, 'votings':votings})


def edit_census(request):

    if request.user.is_staff:
        n_id = request.GET.get('id')
        census = get_object_or_404(Census,id=n_id)

        return render(request, 'edit_census.html',{'census': census})

def save_edited_census(request):
    if request.user.is_staff:
        census_id = request.GET.get('id')
        voting_id = request.GET.get('voting_id')
        voter_id = request.GET.get('voter_id')
        census = get_object_or_404(Census,id=census_id)

        census.voting_id = voting_id
        census.voter_id = voter_id
        census.save()

    else:
        messages.add_message(request, messages.ERROR, "Permission denied")

    return redirect('listCensus')


def add_census(request):

    return render(request, 'add_census.html')

def save_new_census(request):
    if request.user.is_staff:
        census_id = request.GET.get('id')
        voting_id = request.GET.get('voting_id')
        voter_id = request.GET.get('voter_id')
        
        census = Census(voting_id=voting_id, voter_id=voter_id)
        census.save()
    else:
        messages.add_message(request, messages.ERROR, "Permission denied")

    return redirect('listCensus')

def delete_census(request):
    if request.user.is_staff:
        n_id = request.GET.get('id')
        census = get_object_or_404(Census,id=n_id)

        return render(request, 'delete_census.html',{'census': census})
    else:
        messages.add_message(request, messages.ERROR, "Permission denied")

        return redirect('listCensus')

def delete_selected_census(request):

    if request.user.is_staff:
        census_id = request.GET.get('id')
        census = get_object_or_404(Census,id=census_id)
        census.delete()

    else:
        messages.add_message(request, messages.ERROR, "Permission denied")

    return redirect('listCensus')
    
    
def view_voting(request):
    if request.user.is_staff:
        n_id = request.GET.get('id')
        census = get_object_or_404(Census,id=n_id)
        voters = []
        
        voters = get_voters_by_voting_id(voting_id=census.voting_id)

        return render(request, 'view_voting.html',{'census': census ,'voting_id': census.voting_id, 'voters': voters})
    
def get_voters_by_voting_id(voting_id):
    allCensus = Census.objects.all()
    votingSelected_id = voting_id
    voters = []
    
    for cens in allCensus:
        if cens.voting_id == votingSelected_id:
            voters.append(cens.voter_id)
    
    return voters
    
def move_voters_view(request):
    if request.user.is_staff:
        census_id = request.GET.get('id')
        census = get_object_or_404(Census,id=census_id)
        voters = []
        voters = get_voters_by_voting_id(voting_id=census.voting_id)
        votings = []
        for cens in Census.objects.all():
            if cens.voting_id not in votings:
                votings.append(cens.voting_id)
        
        return render(request, 'move_voters.html',{'census': census, 'voting_id': census.voting_id, 'voters': voters, 'votings': votings})     

def move_voters(request):
    census_id = request.GET.get('id')
    votings = request.GET.get('votings')
    voting_id = request.GET.get('voting_id')
    
    allCensus = Census.objects.all()
    census = get_object_or_404(Census,id=census_id)
    if voting_id == '' or int(voting_id) == census.voting_id:
        return redirect('listCensus')
    voters = []
    voters = get_voters_by_voting_id(voting_id=int(voting_id))
    votersToMove = []
    votersToMove = get_voters_by_voting_id(voting_id=census.voting_id)
    
    for voter in votersToMove:
        if voting_id in votings:
            if voter not in voters:
                newCensus = Census(voting_id= voting_id, voter_id=voter)
                newCensus.save()
        else:
                newCensus = Census(voting_id= voting_id, voter_id= voter)
                newCensus.save()
    return redirect('listCensus')    
        
        
        