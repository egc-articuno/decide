import json
from rest_framework.views import APIView
from rest_framework.response import Response

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

def postProcHtml(request):
    #dir_path = os.path.dirname(os.path.realpath("postproc/mock.json"))
    with open("/mnt/c/Users/danie/Desktop/AII Workspace/Decide/decide/decide/postproc/mock.json") as json_file:
        data = json.load(json_file)
    return render(request,"postProcHtml.html",{'options': data})