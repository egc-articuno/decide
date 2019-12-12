from rest_framework.views import APIView
from rest_framework.response import Response
import pgeocode
from bs4 import BeautifulSoup
import urllib.request, re
from django.shortcuts import render

class PostProcView(APIView):

    def identity(self, options):
        out = []

        for opt in options:
            out.append({
                **opt,
                'postproc': opt['votes'],
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    # Este método calcula el resultado en proporcion al numero de votantes por CP de manera que cada provincia que ha votado tiene el mismo poder electoral
    #   Se supone que llegan los votos agrupados por CP segun el siguiente formato:
    #       options: [
    #             {
    #              option: str,
    #              number: int,
    #              votes: {CP(int): int, CP2(int): int},
    #              ...extraparams
    #             }
    #   Como este cálculo es en porcentaje, lo máximo que puede aportar una provincia a una option es 100
    # Sin acabar

    def county(self, options):
        out = []
        county_votes = {}
        nomi = pgeocode.Nominatim('ES')

        for opt in options:
            for cp, votes in opt['votes'].items():
                county = nomi.query_postal_code(cp)['county_name'] #Hay que comprobar esta linea

                if county in county_votes:
                    county_votes[county] = county_votes[county] + opt['votes'][cp]
                else:
                    county_votes[county] = opt['votes'][cp]

        for opt in options:
            result = 0
            for cp, votes in opt['votes'].items():
                county = nomi.query_postal_code(cp)['county_name']
                county_percent = votes / county_votes[county] * 100
                result += county_percent
            out.append({
                **opt,
                'postproc': result,
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

        
    # Este método calcula el resultado de la votación según la comunidad autonoma del candidato, dando mas puntuacion
    # a los que pertenecen a una comunidad con menos poblacion.
    # En las opciones van a llegar los siguientes datos de los candidatos:
    #       options: [
    #             {
    #              option: str,
    #              number: int,
    #              votes: {CP(int): int, CP2(int): int},
    #              ...extraparams
    #             }
    #              cp: int


    def equalityMunicipality(self, options):
        out = []
        county_votes = {}
        nomi = pgeocode.Nominatim('ES')
        
        url="https://en.wikipedia.org/wiki/Ranked_lists_of_Spanish_municipalities"
        fichero = "municipilaties"
        f = urllib.request.urlretrieve(url,fichero)
        f = open (fichero, encoding="utf-8")
        s = f.read()
        soup = BeautifulSoup(s, "html.parser")
        rows = soup.find("table").find('tbody').findAll("tr")

        mapping = {}
        for row in rows:
            poblation = 0
            city = ""
            i = 0
            row = row.findAll("td")
            for element in row:
                i+=1
                if i==2:
                    city = element.find("a").text.rstrip()
                if i==4:
                    poblation=element.text.rstrip()
            mapping[city]=poblation

        for opt in options:
            votes = opt['votes'] 
            votes = votes + votes*(0.1*(mapping[nomi.query_postal_code(opt['cp'])['community_name']]))
            out.append({
                **opt,
                'postproc': votes,
            });
        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

    def post(self, request):
        """
         * type: IDENTITY | EQUALITY | WEIGHT
         * options: [
            {
             option: str,
             number: int,
             votes: int,
             ...extraparams
            }
           ]
        """

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)

        elif t == 'COUNTY_EQUALITY':
            return self.county(opts)
        elif t == "EQUALITY_MUNICIPALITY":
            return self.equalityMunicipality(opts)

        return Response({})

def postProcHtml(request):
    return render(request,"postProcHtml.html",{})


