import json
from rest_framework.views import APIView
from rest_framework.response import Response
import pgeocode

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

    def parity(self, options):
        out = []
        outMale = []
        outFemale = []

        for opt in options:
            if (opt['gender'] == 0):
                outFemale.append({
                    **opt,
                    'postproc': opt['votes'], })
            else:
                outMale.append({
                    **opt,
                    'postproc': opt['votes'], })

        outMale.sort(key=lambda x: -x['postproc'])
        outFemale.sort(key=lambda x: -x['postproc'])
        size=0
        sizeSmall = len(outMale)
        sizeBigger = len(outFemale)
        if len(outFemale)<len(outMale):
            size=1
            sizeSmall=len(outFemale)
            sizeBigger=len(outMale)

        if outMale[0]['votes']>=outFemale[0]['votes']:
            for i in range(0, sizeSmall):
                    out.append(outMale[i])
                    out.append(outFemale[i])

        else:
            for i in range(0, sizeSmall):
                    out.append(outFemale[i])
                    out.append(outMale[i])

        if size==0:
            for i in range(sizeSmall, sizeBigger):
                out.append(outFemale[i])
        return Response(out)

    def weigth_per_gender(self, options):
        outMale = []
        outFemale = []

        for opt in options:
            opt['votesFemale'] = opt['votesFemale'] * 2
            outFemale.append({**opt, 'postprocFemale': opt['votesFemale'] })
            opt['votesMale'] = opt['votesMale'] * 1
            outMale.append({**opt, 'postprocMale': opt['votesMale'] })

        return Response(outMale, outFemale)

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

        t = request.data.get('type', 'GENDER')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)
        elif t == 'PARITY':
            return self.parity(opts)
        elif t == 'GENDER':
            return self.weigth_per_gender(opts)

        elif t == 'COUNTY_EQUALITY':
            return self.county(opts)

        return Response({})

def postProcHtml(request):
    #dir_path = os.path.dirname(os.path.realpath("postproc/mock.json"))
    with open("/mnt/c/Users/danie/Desktop/AII Workspace/Decide/decide/decide/postproc/mock.json") as json_file:
        data = json.load(json_file)
    return render(request,"postProcHtml.html",{'options': data})