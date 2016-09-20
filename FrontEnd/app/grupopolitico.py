from app.server import server
from app.menus import menus
from django.shortcuts import render
from django.http import *
from django.template import RequestContext
from django.shortcuts import *
from django.core import serializers
from . import views
from SILPCache import SILPCache
import requests
import math

"""description of class"""
def getListGP(request):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata  = x.getContent(endereco+'getpoliticalgroups/1/100', 4)
    XMLdataY = menus.getCommittesMenu(request) #obtem dados do servi�o getcommittes
    XMLMenuMinisterio = menus.getMinisteriesMenu(request)
    XMLGroupPolitico = menus.getGruposMenu(request)
    response_feed = views.getFeed(request)#obt�m dados de feed proveniente de http://asemana.sapo.cv

    context = {'lista': XMLdata, 'feed':  str(response_feed.content, encoding='utf-8'), 'committes': XMLdataY, 'ministeries': XMLMenuMinisterio, 'grupoPolitico': XMLGroupPolitico}
    #return render_to_response('grupos_politicos.html', context, context_instance=RequestContext(self))
    return render(request,'app/grupos_politicos.html', context)

#retorna total de membros de um determinado grupo politico
def getTotalNumberMember(request, IDGroup):
    url = server.ServerEndereco(request)
    response = requests.get(url+'getpoliticalgroupmemberscount/'+IDGroup)
    result = response.json()

    TotalCount = math.ceil(result[0]['numberofmembers_'])

    return TotalCount

    # retorna lista de grupos politicos
def getGrupoPolitico(request,IdGpolitico):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLGroup = x.getContent(endereco+'getgroup/'+IdGpolitico,0)
    XMLdata = x.getContent(endereco+'getpoliticalgroupmembers/1/9/'+IdGpolitico,0)
    XMLdataY = menus.getCommittesMenu(request) #obtem dados do servi�o getcommittes
    XMLMenuMinisterio = menus.getMinisteriesMenu(request)
    XMLGroupPolitico = menus.getGruposMenu(request)
    TotalMember = getTotalNumberMember(request, IdGpolitico)

    context = {'Group': XMLGroup, 'GrupoPoliticoMember': XMLdata, 'feed':  '', 'committes':  XMLdataY, 'idGrup': IdGpolitico, 'ministeries': XMLMenuMinisterio, 'grupoPolitico': XMLGroupPolitico,'TotalMembers': TotalMember}
    #return render_to_response('GrupoPolitico.html', context, context_instance=RequestContext(self))
    return render(request,'app/GrupoPolitico.html', context)

#retorna lista de grupos politicos apartir de pagina��o
def MemberGroupList(request, LimitInfI,NumberElements, IdGroup):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'getpoliticalgroupmembers/'+LimitInfI+'/'+NumberElements+'/'+IdGroup,0)
    x.getImage(XMLdata)

    return HttpResponse(XMLdata)


