from app.server import server
from app.menus import menus
from django.shortcuts import render
from django.http import *
from django.template import RequestContext
from django.shortcuts import *
from django.core import serializers
from SILPCache import SILPCache
import requests
import math

#Retorna total de Documentos
def getTotalNumberMemberCommittes(request, idCommittes):
    url = server.ServerEndereco(request)
    response = requests.get(url+'getcommitteememberscount/'+idCommittes)
    result = response.json()

    TotalCount = math.ceil(result[0]['numberofmembers_'])

    return TotalCount

#retorna membros de comiss�es
def getCommittesMembers(request,IdCommittes):
    x = SILPCache('cache')
    endereco = server.ServerEndereco('')
    XMLCommitte = x.getContent(endereco+'getgroup/'+IdCommittes,0)
    XMLdata = x.getContent(endereco+'getcommitteemembers/1/9/'+IdCommittes,0)
    XMLdataY = menus.getCommittesMenu(request) #obtem dados do servi�o getcommittes
    XMLMenuMinisterio = menus.getMinisteriesMenu(request)
    XMLGroupPolitico = menus.getGruposMenu(request)
    TotalCountMember = getTotalNumberMemberCommittes(request,IdCommittes)

    context = {'Committee':XMLCommitte, 'CommittesMembers': XMLdata, 'feed':  '', 'committes':  XMLdataY,'idComicao': IdCommittes, 'ministeries': XMLMenuMinisterio, 'grupoPolitico': XMLGroupPolitico, 'TotalCountMember':TotalCountMember}
    #return render_to_response('CommittesMembers.html', context, context_instance=RequestContext(self))
    return render(request,'app/CommittesMembers.html', context)

#retorna membros de uma determinada comiss�o
def CommittesMemberList(request, LimitInfI, LimitSup, IdCommittes):
    x = SILPCache('cache')
    endereco = server.ServerEndereco('')
    XMLdata = x.getContent(endereco+'getcommitteemembers/'+LimitInfI+'/'+LimitSup+'/'+IdCommittes,0)
    x.getImage(XMLdata)

    return HttpResponse(XMLdata)



