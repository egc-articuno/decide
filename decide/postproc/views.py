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

          

    def hondt(self, options, nSeats):
        parties = [] # Partidos politicos - option
        points = [] #Puntos de cada partido - votes
        seats = [] #Salida - se almacena en dicha lista el valor calculado de los escaños
        out = []

        for i in options:
            esc = 0
            seats.append(esc)

        for opt in options:
            parties.append(opt['votes']) #Copia 
            #Concatenar el número de votos con la opción
            out.append({
                **opt,
                'seats': 0,
                });
        #Número de escaños totales
        points = parties
        seatsToDistribution = nSeats 
        
        def giveASeat():
            biggest = max(points)
            index = points.index(biggest)
            seats[index] += 1
            out[index]['seats'] += 1
            points[index] = parties[index] / (seats[index]+1)

        for i in range(0,seatsToDistribution):
            giveASeat()
            

        out.sort(key=lambda x: -x['seats'])
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

        elif t == 'HONDT':
            return self.hondt(opts,request.data.get('nSeats'))
        return Response({})

def postProcHtml(request):
    return render(request,"postProcHtml.html",{})