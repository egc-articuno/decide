import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
import pgeocode
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

    # Este método realiza ponderaciones a los pesos de los votos dependiendo del género del votante en cuestión
    #   Se supone que llegan el número de votos de hombres y mujeres para cada candidato y la ponderación dada para cada género:
    #       options: [
    #             {
    #              option: str,
    #              number: int,
    #              votesFemale: int,
    #              pondFemale: int,
    #              votesMale: int,
    #              pondMale: int,
    #              ...extraparams
    #             }
    # El método dará un peso u otro a los votos de hombres y mujeres dependiendo del género, y finalmente sumará
    # ambos para realizar el conteo final para cada candidato.
    # Por mejorar
    def weigth_per_gender(self, options):
        out = []    # JSON esperado en la salida
        votesFinal = 0  # Acumulador donde se guardará el recuento de los votos tras la ponderación por género
        try:
            for opt in options:
                votesFinal = (opt['votesFemale'] * opt['pondFemale']) + (opt['votesMale'] * opt['pondMale'])
                out.append({**opt, 'postproc': votesFinal })
        except:
            print("An exception occurred in the expected data in the weigth_per_gender method")
            out.append({'error': 'An exception occurred in the expected data in the weigth_per_gender method'})

        return Response(out)

    #   Este método lo que hace es agrupar a los votantes entre distintos rangos de edad, y a cada rango asignarle un peso de modo que el resultado sea una ponderación
    #   de los votos con un peso de edad a partir del dato original
    #   Se supone que llegan los votos agrupados por ageRange segun el siguiente formato:
    #       options: [
    #             {
    #               .
    #               .
    #               .
    #              ageRange: {RANGE(string): int, RANGE2(string): int, ... , RANGE8(string): int},
    #               .
    #               .
    #               .
    #             }
    def voter_weight_age(self, options):
        out = [] # JSON esperado en la salida
        result = 0 # Acumulador donde se guardará el recuento de los votos tras la ponderación por edad
        i = 1
        for opt in options:
            votesAges = opt['ageRange']
            for a in votesAges:
                if votesAges.get(a)<0 or len(votesAges)<8:
                        print("An exception occurred in the expected data in the voter_weight_age method")
                        out.append({'error': 'An exception occurred in the expected data in the voter_weight_age method'})
                        return Response(out)
                else:
                    result += i * votesAges.get(a)
                    i = i + 1
            i = 1
            out.append({**opt, 'postproc': result})
            result = 0

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

    def county(self, options):
        out = []
        county_votes = {}
        nomi = pgeocode.Nominatim('ES')

        for opt in options:
            for cp, votes in opt['votes'].items():
                county = nomi.query_postal_code(cp)['county_name']

                if county in county_votes:
                    county_votes[county] = county_votes[county] + opt['votes'][cp]
                else:
                    county_votes[county] = opt['votes'][cp]

        for opt in options:
            result = 0
            for cp, votes in opt['votes'].items():
                county = nomi.query_postal_code(cp)['county_name']
                county_percent = round(votes / county_votes[county] * 100)
                result += county_percent
            out.append({
                **opt,
                'postproc': result,
            });

        out.sort(key=lambda x: -x['postproc'])
        return Response(out)

          
#Sistema D'Hondt - Metodo de promedio mayor para asignar escaños en sistemas de representación proporcional por listas electorales. Por tanto,
# en dicho método trabajaremos con listas de partidos politicos y con un número de escaños que será pasado como parámetro. 
    #       nSeats: 10
    #       options: [
    #             {
    #              option: Partido1,
    #              number: 1,
    #              votes: 5,
    #        
    #             } {
    #              option: Partido2,
    #              number: 2,
    #              votes: 3,
    #              }.
    #               .

    def hondt(self, options, nSeats):
        parties = [] # Partidos politicos - option
        points = [] #Puntos de cada partido - votes
        seats = [] #Escaños por partidos
        out = [] #Salida

        #Calcular el número de escaño que voy a tener según el número de partidos, inicializamos a 0
        for i in options:
            esc = 0
            seats.append(esc)


        for opt in options:
            parties.append(opt['votes']) #Copia de los votos de cada partido
            #Concatenar la parametros de Opt con seats para mostrarlo en la salida
            out.append({
                **opt,
                'seats': 0,
                })
        points = parties
        seatsToDistribution = nSeats 
        
        #Submétodo para asignar los escaños
        # En cada iteración se calcula los cocientes para cada partido y se asigna un escaño al partido con cociente mayor. Para la siguiente iteracion se recalcula
        #  el cociente del partido que acaba de recibir un escaño. Los demas partidos mantienen su cociente ya que no reciben escaño y se repite el proceso.
        def giveASeat():
            biggest = max(points) #Obtener el partido con mayor número de votos
            index = points.index(biggest)
            if biggest != 0:
                
                seats[index] += 1 
                out[index]['seats'] += 1 
                points[index] = parties[index] / (seats[index]+1) 

        #Llamar al método de asignación de escaños tantas veces como número de escaños tengamos
        for i in range(0,seatsToDistribution):
            giveASeat()
            
        #Ordeno los resultados de la salida por el número de escaños
        out.sort(key=lambda x: -x['seats'])
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
            if len(options)==0:
                print("An exception occurred with equality province method")
                out.append({'error': 'The Data is empty'})
        except:
            if len(options)>0:
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
        elif t == 'AGERANGE':
            return self.voter_weight_age(opts)
        elif t == 'COUNTY_EQUALITY':
            return self.county(opts)
        elif t == "EQUALITY_PROVINCE":
            return self.equalityProvince(opts)

        elif t == 'HONDT':
            return self.hondt(opts,request.data.get('nSeats'))
        return Response({})

def postProcHtml(request):
    p = PostProcView()
    dir_path = os.path.dirname(os.path.realpath(__file__))
    with open(dir_path + "/mock.json", "r", encoding="utf-8") as json_file:
        data = json.load(json_file)
        opts = json.dumps(data)
        opts = data[0]['options']
        result = p.voter_weight_age(opts)
        result.accepted_renderer = JSONRenderer()
        result.accepted_media_type = "application/json"
        result.renderer_context = {}
        result = result.render()
        result = result.content.decode("utf-8")
        result = json.loads(result)
        r = []
        for res in result:
            r.append(res['postproc'])
    return render(request,"postProcHtml.html",{'options': r})
