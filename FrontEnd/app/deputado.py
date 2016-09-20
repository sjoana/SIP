from app.server import server
from app.menus import menus
from django.shortcuts import render
from django.http import *
from django.template import RequestContext
from django.shortcuts import *
from django.core import serializers
from . import views
import math
from SILPCache import SILPCache
import requests

"""description of class"""
def getTotalNumberMember(request, status):
    url = server.ServerEndereco(request)
    response = requests.get(url+'getmemberscount')
    result = response.json()

    TotalCount = math.ceil(result[0]['numberofmembers_'])
    if(status != 0): #caso status for diferente de 0 devolve total para ajax
        return HttpResponse(TotalCount)
    else: # caso status for 0 devove total para ser usado em outros metodos
        return TotalCount

#Retorna a lista de Deputados
def getMembers(request):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata  = x.getContent(endereco+'getmembers/1/9',4)
    x.getImage(XMLdata)
    response_feed = views.getFeed(request)
    XMLdataY = menus.getCommittesMenu(request)
    XMLMenuMinisterio = menus.getMinisteriesMenu(request)
    XMLGroupPolitico = menus.getGruposMenu(request)
    totalMember = getTotalNumberMember(request, 0)
    Partidos = views.getAllParty(request)

    context = {'partido': Partidos, 'lista': XMLdata, 'feed': str(response_feed.content, encoding='utf-8'),'committes': XMLdataY, 'ministeries': XMLMenuMinisterio, 'grupoPolitico': XMLGroupPolitico, 'TotalMember': totalMember}
    #return render_to_response('members.html', context, context_instance=RequestContext(self))
    return render(request,'app/members.html', context)

#Retorna a lista de Deputados Já com um determinado limite de dados
def DeputadoList(request, LimitInf, LimitSup):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'getmembers/'+LimitInf+'/'+LimitSup+'',4)
    x.getImage(XMLdata)

    return HttpResponse(XMLdata)

#Retorna dados de um determinado Membro
def getMember(request,IDMember):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'getmember/'+IDMember,4)
    x.getImage(XMLdata)
    context = XMLdata

    return HttpResponse(context)

#Retorna dados de Membros atravéz de Pesquisa por(Nome ou Partido)
def getMemberSearch(request, LimitInf, LimitSup, Name, partido):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'getmembersearch/'+LimitInf+'/4/'+Name+'/'+partido,4)
    x.getImage(XMLdata)
    context = XMLdata

    return HttpResponse(context)

#Retorna Total de Membros
def getMemberSearchCount(request, Name, partido):
    url = server.ServerEndereco(request)
    response = requests.get(url+'getmembersearchcount/'+Name+'/'+partido)
    result = response.json()
    TotalCount = math.ceil(int(result[0]['numberofmembers']))

    return HttpResponse(TotalCount)

#Retorna dados de Utilizador
def getUser(request,IDMember):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'getuser/'+IDMember,4)
    x.getImage(XMLdata)
    context = XMLdata

    return HttpResponse(context)

