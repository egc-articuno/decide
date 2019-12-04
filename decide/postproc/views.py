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

        return Response({})

def postProcHtml(request):
    #dir_path = os.path.dirname(os.path.realpath("postproc/mock.json"))
    with open("/mnt/c/Users/danie/Desktop/AII Workspace/Decide/decide/decide/postproc/mock.json") as json_file:
        data = json.load(json_file)
    return render(request,"postProcHtml.html",{'options': data})