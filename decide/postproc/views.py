from rest_framework.views import APIView
from rest_framework.response import Response
import pgeocode

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
                    county_votes[county] += opt['votes']
                else:
                    county_votes[county] = opt['votes']

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

        t = request.data.get('type', 'IDENTITY')
        opts = request.data.get('options', [])

        if t == 'IDENTITY':
            return self.identity(opts)

        elif t == 'COUNTY_EQUALITY':
            return self.county(opts)

        return Response({})
