from rest_framework.views import APIView
from rest_framework.response import Response


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
            if (opt['gender']):
                outFemale.append({
                    **opt,
                    'postproc': opt['votes'], })
            else:
                outMale.append({
                    **opt,
                    'postproc': opt['votes'], })
        # Se ordenan ambas listas
        outMale.sort(key=lambda x: -x['postproc'])
        outFemale.sort(key=lambda x: -x['postproc'])







        while len(outMale)>0 and len(outFemale)>0:
            aux = []
            for i in range(0, 3):
                aux.append(outMale[i])
                aux.append(outFemale[i])
            aux.sort(key=lambda x: -x['postproc'])
            aux.remove(aux[5])
            for a in aux:
                out.append(a)
                if outMale.__contains__(a):
                    outMale.remove(a)
                if outFemale.__contains__(a):
                    outFemale.remove(a)

        out.append(outFemale)
        out.append(outMale)

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
        elif t == 'PARITY':
            return self.parity(opts)

        return Response({})
