"""
Definition of views.
"""

from django.shortcuts import render
from django.http import *
from django.template import RequestContext
from django.shortcuts import *
from django.core import serializers
from datetime import datetime
import xml.etree.ElementTree
import xmltodict
import os
import json
from SILPCache import SILPCache
from app.server import server
from . import views
from app.menus import menus
import requests

#retorna a ultima legislatura
def getIdlegislatura(request):
    url = server.ServerEndereco(request)
    response = requests.get(url+'getactivelegislature/1/100')
    result = response.json()
    return result[0]['group_id']


#retorna a legislativa atual
def getCourentLegislature(request):
    x=SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = requests.get(endereco+'getactivelegislature/1/1')
    result = XMLdata.json()
    return result[0]['group_id']

#retorna o serviço do asemana.sapo.cv
def getFeed(request):
    try :
        response_feed = requests.get('http://services.sapo.pt/rss/feed/homepage/tl/por/geral')
    except :
        response_feed =  HttpResponse('Não foi possível aceder a notícias')
    return response_feed

#busca os dados dos partido
def getAllParty(request):
    endereco = server.ServerEndereco(request)
    response = requests.get(endereco+'getpartys')
    result = response.json()

    return result

def getHome(request):
    x = SILPCache('C:/tmp/cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'getactivelegislature/1/1',4)
    XMLdataY = menus.getCommittesMenu(request) #obtem dados do serviço getcommittes
    XMLMenuMinisterio = menus.getMinisteriesMenu(request)
    XMLGroupPolitico = menus.getGruposMenu(request)
    response_feed = views.getFeed(request) #obtém dados de feed proveniente de http://asemana.sapo.cv
    JsonWokflows = views.dicionaryWorkflowDocument(request)

    context = {'legislatura': XMLdata, 'feed': str(response_feed.content, encoding='utf-8'),'committes': XMLdataY, 'ministeries': XMLMenuMinisterio, 'grupoPolitico': XMLGroupPolitico,'workflow': JsonWokflows}
    #return render_to_response('home.html', context, context_instance=RequestContext(self))
    return render(request,'app/home.html', context)
    
#gera pesquisa avançada
def getPesquisaAvancada(request):
    XMLdataY = menus.getCommittesMenu(request) #obtem dados do serviço getcommittes
    XMLMenuMinisterio = menus.getMinisteriesMenu(request)
    XMLGroupPolitico = menus.getGruposMenu(request)
    esponse_feed = views.getFeed(request) #obtém dados de feed proveniente de http://asemana.sapo.cv

    context = {'feed':  str(esponse_feed.content, encoding='utf-8'), 'committes':  XMLdataY, 'ministeries': XMLMenuMinisterio, 'grupoPolitico': XMLGroupPolitico}
    #return render_to_response('pesquisa_avacada.html', context, context_instance=RequestContext(self))
    return render(request,'app/pesquisa_avacada.html', context)

#retorna resultado da pesquisa avançada
def getResultadoPesquisaAvancada(request, endpoint, parametros): #parametros contém valores referente a documento, todo documento e interveniente
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+endpoint+'/1/100/'+parametros,0)

    return HttpResponse(XMLdata)

#gera pesquisa
def getPesquisa(request):
    endereco = server.ServerEndereco(request)
    XMLdataY = menus.getCommittesMenu(request) #obtem dados do serviço getcommittes
    XMLMenuMinisterio = menus.getMinisteriesMenu(request)
    XMLGroupPolitico = menus.getGruposMenu(request)
    esponse_feed = views.getFeed(request) #obtém dados de feed proveniente de http://asemana.sapo.cv

    valueSearch = self.GET['srch-term']

    result = requests.get(endereco+'getcompletesearch/1/100/'+valueSearch)

    context = {'feed':  str(esponse_feed.content, encoding='utf-8'), 'committes':  XMLdataY, 'ministeries': XMLMenuMinisterio, 'grupoPolitico': XMLGroupPolitico,'XMLdata': result}
    #return render_to_response('pesquisa.html', context, context_instance=RequestContext(self))
    return render(request,'app/pesquisa.html', context)

def getCalendar(request):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'getscheduleditems/1/100',0)
    XMLdataY = menus.getCommittesMenu(request) #obtem dados do serviço getcommittes
    XMLMenuMinisterio = menus.getMinisteriesMenu(request)
    XMLGroupPolitico = menus.getGruposMenu(request)

    context = {'agendamentos': XMLdata, 'committes': XMLdataY,'committes': XMLdataY, 'ministeries': XMLMenuMinisterio, 'grupoPolitico': XMLGroupPolitico}
    #return render_to_response('calendar.html', context, context_instance=RequestContext(self))
    return render(request,'app/calendar.html', context)

#Cria json com estados de cada Workflows
def dicionaryWorkflow(request):
    path = r'workflows'  # remove the trailing '\'
    data = []
    i=0
    WorkFlowFinal = dict()
    WorkFlowFinal['agenda_text_record']='Agendamento'

    for dir_entry in os.listdir(path):
        dir_entry_path = os.path.join(path, dir_entry)
        if os.path.isfile(dir_entry_path):
            data.append(dir_entry_path)
            while (i<len(data)):
                fp = open(data[i], 'r')
                dados = fp.read()
                dataJson = xmltodict.parse(dados)
                tam = len(dataJson['workflow']['state'])
                s = 0
                while (s<tam):
                    WorkFlow = dict(dataJson['workflow']['state'][s])
                    WorkFlowFinal[WorkFlow['@id']]=WorkFlow['@title']
                    s=s+1

                WorkFlowFinal[dir_entry[:-4]] = dataJson['workflow']['@title']
                i=i+1


    return json.dumps(WorkFlowFinal)

#Cria dicionario com descrição de documentos para ser alimentado na local store
def dicionaryWorkflowDocument(request):
    path = r'workflows'  # remove the trailing '\'
    data = []
    i=0
    WorkFlowFinal = dict()
    WorkFlowFinal={'committee': 'Comissão','plenary': 'Plenário', 'agenda_text_record': 'Agendamento'}
    for dir_entry in os.listdir(path):
        dir_entry_path = os.path.join(path, dir_entry)
        if os.path.isfile(dir_entry_path):
            data.append(dir_entry_path)
            while (i<len(data)):
                fp = open(data[i], 'r')
                dados = fp.read()
                dataJson = xmltodict.parse(dados)
                tam = len(dataJson['workflow']['state'])

                WorkFlowFinal[dir_entry[:-4]] = dataJson['workflow']['@title']
                i=i+1

    return json.dumps(WorkFlowFinal)


#imprime tramite em pdf
def printPDF(request,IdTramite):
    endereco = server.ServerEndereco(request)
    result = requests.get(endereco+'document2pdf/'+IdTramite)
    response = HttpResponse(content_type='application/pdf',content=result.content)

    return response

#direciona o utilizador para o site do parlamento.cv
def siteParlamento(request):
    return HttpResponseRedirect('http://www.parlamento.tl')

def siteParlamentoEspacoCidadao(request):
    return HttpResponseRedirect('http://www.parlamento.tl')