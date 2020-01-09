import json
from rest_framework.views import APIView
from rest_framework.response import Response
import pgeocode
from bs4 import BeautifulSoup
import urllib.request, re
from django.shortcuts import render
import os 

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

    def parity(self, options):
        out = []
        # Se crea una lista para los candidatos hombres y otra para las mujeres
        outMale = []
        outFemale = []

        # Se añaden a cada lista las opciones, dependiendo del genero
        for opt in options:
            if (opt['gender'] == 'F'):
                outFemale.append(opt)

            elif(opt['gender'] == 'M'):
                outMale.append(opt)

        # Se ordenan ambas listas
        outMale.sort(key=lambda x: -x['votes'])
        outFemale.sort(key=lambda x: -x['votes'])

        while len(outMale) > 0 and len(outFemale) > 0:
            aux = []
            for i in range(0, 3):
                aux.append(outMale[i])
                aux.append(outFemale[i])
            aux.sort(key=lambda x: -x['votes'])
            aux.remove(aux[5])
            for a in aux:
                out.append(a)
                if a in outMale:
                    outMale.remove(a)
                if a in outFemale:
                    outFemale.remove(a)
        for o in outMale:
            out.append(o)
        for o in outFemale:
            out.append(o)

        return Response(out)

    def weigth_per_gender(self, options):
        out = []
        votesFinal = 0

        for opt in options:
            votesFinal = (opt['votesFemale'] * 2) + (opt['votesMale'] * 1)
            out.append({**opt, 'postproc': votesFinal })

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


    def get_map(self):
        res = {}

        try:
            dir_path = os.path.dirname(os.path.realpath(__file__))
            f=open(dir_path+"/provincias", "r", encoding="utf-8")
            lines = f.readlines()
            for line in lines:
                provincia = line.split(",")
                res[provincia[1].rstrip().strip()]=provincia[0]
        except:
            print('An except ocurred reading the province list file')
        return res


    def equalityProvince(self, options):
        out = []
        county_votes = {}
        nomi = pgeocode.Nominatim('ES')
        mapping = self.get_map()
        try:
            for opt in options:
                print(opt)
                votes = opt['votes'] 
                coef = float(0.01)
                position = float((mapping[nomi.query_postal_code(opt['postal_code'])['county_name']]))
                votes = float(votes) + float(votes)*coef*position
                votes = int(votes)
                out.append({
                    **opt,
                    'postproc': votes,
                })
            out.sort(key=lambda x: -x['postproc'])
        except:
            print("An exception occurred with equality province method")
            out.append({'error': 'An exception occurred with equality province method'})

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

        t = request.data.get('type', 'EQUALITY_PROVINCE')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'PARITY':
            return self.parity(opts)
        elif t == 'GENDER':
            return self.weigth_per_gender(opts)
        elif t == 'COUNTY_EQUALITY':
            return self.county(opts)
        elif t == "EQUALITY_PROVINCE":
            return self.equalityProvince(opts)

        return Response({})

def postProcHtml(request):
    #dir_path = os.path.dirname(os.path.realpath("postproc/mock.json"))
    with open("/mnt/c/Users/danie/Desktop/AII Workspace/Decide/decide/decide/postproc/mock.json") as json_file:
        data = json.load(json_file)
    return render(request,"postProcHtml.html",{'options': data})
