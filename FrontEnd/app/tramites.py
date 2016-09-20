from django.shortcuts import render
from django.http import *
from django.template import RequestContext
from django.shortcuts import *
from django.core import serializers
import math
import datetime
import xml.etree.ElementTree
from . import views
from app.server import server
from app.menus import menus
from SILPCache import SILPCache
import requests

"""description of class"""
#retorna total de documentos em tramite
def getTotalTramites(request, idTramite):
    url = server.ServerEndereco(request)
    response = requests.get(url+'documentstypecount/'+idTramite)
    result = response.json()

    TotalCount = math.ceil(result[0]['numberofmembers_'])

    return TotalCount

#gera modal para doc Leis
def getDocLeiModal(request,IdDocLei):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'documenthistory/1/100/'+IdDocLei,0)
    JsonWokflows = views.dicionaryWorkflow(request)

    XMLdataY = menus.getCommittesMenu(request) #obtem dados do serviço getcommittes
    XMLmenusMinisterio = menus.getMinisteriesMenu(request)
    XMLGroupPolitico = menus.getGruposMenu(request)
    response_feed = views.getFeed(request) #obtém dados de feed proveniente de http://asemana.sapo.cv

    context = {'documenthistory': XMLdata, 'workflow': JsonWokflows, 'DocId': IdDocLei, 'committes': XMLdataY, 'ministeries':XMLmenusMinisterio, 'grupoPolitico': XMLGroupPolitico, 'feed': str(response_feed.content, encoding='utf-8')}

    #return render_to_response('docLeiModal.html', context, context_instance=RequestContext(request))
    return render(request,'app/docLeiModal.html', context)

#Retorna Total de Documento em Tramites
def getTotalDocumentTramite(request,datas):
    if(datas == ''):
        data_1 = datetime.datetime.now()
        end_date = data_1 + datetime.timedelta(days=7)
        datas = str(data_1.strftime('%d-%m-%Y'))+'/'+str(end_date.strftime('%d-%m-%Y'))

    url = server.ServerEndereco(request)
    response = requests.get(url+'getscheduleditemscount/'+datas)
    result = response.json()

    TotalCount = math.ceil(result[0]['numberofitems_'])

    return TotalCount

#Retorna lista de Tramites
def getTramiteList(request, LimitInf,LimitSup, IdTramite):
    x        = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata  =   x.getContent(endereco+'getdocsbytype/'+LimitInf+'/'+LimitSup+'/'+IdTramite,0)

    return HttpResponse(XMLdata)

def getAllTramiteList(request, LimitInf, NumberElements, IDLegislatura, IDMember):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'getdocsfromuser/'+LimitInf+'/'+NumberElements+'/'+IDLegislatura+'/'+IDMember,0)

    return HttpResponse(XMLdata)

#Retorna Total de Iniciativas
def getTotalIniciativa(request, IDLegislatura, IDMember):
    url = server.ServerEndereco(request)
    response = requests.get(url+'getdocsfromusercount/'+str(IDLegislatura)+'/'+str(IDMember))
    result = response.json()

    TotalCount = math.ceil(result[0]['numberofdocs'])

    return TotalCount

#retorna todos tramites com data marcada para hoje ou próxima semana
def getTramites(request):
    data_1 = datetime.datetime.now()
    end_date = data_1 + datetime.timedelta(days=7)
    datas = str(data_1.strftime('%d-%m-%Y'))+'/'+str(end_date.strftime('%d-%m-%Y'))

    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'getscheduleditems/1/4/'+datas,0)
    response_feed = views.getFeed(request)
    #TotalDoc = tramites.getTotalDocumentTramite('')
    TotalDoc = getTotalDocumentTramite(request,'')
    JsonWokflows = views.dicionaryWorkflowDocument(request)
    context = {'DocProgramado': XMLdata, 'feed':  str(response_feed.content, encoding='utf-8'),'TotalDoc': TotalDoc,'workflow': JsonWokflows}

    #return render_to_response('tramite.html',context, context_instance=RequestContext(request))
    return render(request,'app/tramite.html', context)

#retorna todos tramites numa determinada data
def getTramitesDocumento(request,datas,LimitInfI):
    if datas == '0-00-0000/0-00-0000':
        data_1 = datetime.datetime.now()
        end_date = data_1 + datetime.timedelta(days=7)
        datas = str(data_1.strftime('%d-%m-%Y'))+'/'+str(end_date.strftime('%d-%m-%Y'))

    x        =   SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata  =   x.getContent(endereco+'getscheduleditems/'+LimitInfI+'/4/'+datas,0)
    #TotalDoc = tramites.getTotalDocumentTramite(datas)
    TotalDoc = getTotalDocumentTramite(request,datas)

    dados = xml.etree.ElementTree.fromstring(XMLdata)
    total = xml.etree.ElementTree.SubElement(dados, 'TotalDoc')
    total.text = str(TotalDoc)

    return HttpResponse(xml.etree.ElementTree.tostring(dados), content_type='text/xml')

#Retorna lista de tramites com paginação
def getDocTramite(request,data,LimitInfI):

    if (data == '0-00-0000/0-00-0000'):
        data_1 = datetime.datetime.now()
        end_date = data_1 + datetime.timedelta(days=7)
        data = str(data_1.strftime('%d-%m-%Y'))+'/'+str(end_date.strftime('%d-%m-%Y'))

    x               =   SILPCache('cache')
    endereco        = server.ServerEndereco(request)
    IdLegislatura   = views.getIdlegislatura(request)

    XMLdata         =   x.getContent(endereco+'groupsittings/'+LimitInfI+'/4/'+str(IdLegislatura)+'/'+data,0)
    #TotalDoc = tramites.getTotalDocumentTramite(data)
    TotalDoc = getTotalDocumentTramite(request,data)

    dados = xml.etree.ElementTree.fromstring(XMLdata)
    total = xml.etree.ElementTree.SubElement(dados, 'TotalDoc')
    total.text = str(TotalDoc)
    xml.etree.ElementTree.dump(dados)

    return HttpResponse(xml.etree.ElementTree.tostring(dados), content_type='text/xml')

#retorna Leis
def getDocLei(request,IdDocLei):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'documenthistory/1/100/'+IdDocLei,0)

    jsonWorkflow = views.dicionaryWorkflow(request)

    context = {'documenthistory': XMLdata, 'workflow': jsonWorkflow,'DocId': IdDocLei}
    #return render_to_response('doclei.html', context, context_instance=RequestContext(request))
    return render(request,'app/doclei.html', context)

#Retorna lista de perguntas
def getDocPerguntas(request,IdDocPergunta):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'documenthistory/1/100/'+IdDocPergunta,0)

    jsonWorkflow = views.dicionaryWorkflow(request)

    context = {'documenthistory': XMLdata, 'workflow': jsonWorkflow,'DocId': IdDocPergunta}
    #return render_to_response('docpergunta.html', context, context_instance=RequestContext(request))
    return render(request,'app/docpergunta.html', context)

#gera modal para perguntas
def docPerguntaModal(request,IdDocPergunta):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'documenthistory/1/100/'+IdDocPergunta,0)
    XMLdataY = menus.getCommittesMenu(request) #obtem dados do serviço getcommittes
    XMLmenusMinisterio = menus.getMinisteriesMenu(request)
    XMLGroupPolitico = menus.getGruposMenu(request)
    response_feed = views.getFeed(request) #obtém dados de feed proveniente de http://asemana.sapo.cv

    jsonWorkflow = views.dicionaryWorkflow(request)

    context = {'documenthistory': XMLdata, 'workflow': jsonWorkflow, 'DocId': IdDocPergunta, 'committes': XMLdataY, 'ministeries':XMLmenusMinisterio, 'grupoPolitico': XMLGroupPolitico, 'feed': str(response_feed.content, encoding='utf-8')}
    #return render_to_response('docPerguntaModal.html', context, context_instance=RequestContext(request))
    return render(request,'app/docPerguntaModal.html', context)

#
def getPerguntas(request):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'getdocsbytype/1/4/'+str(2),0)
    #TotalPerguntas = tramites.getTotalTramites(request, str(2))
    TotalPerguntas = getTotalTramites(request, str(2))
    jsonWorkflow = views.dicionaryWorkflow(request)

    context = {'feed':  XMLdata,'TotalPerguntas': TotalPerguntas, 'workflow': jsonWorkflow}

    #return render_to_response('perguntas.html',context, context_instance=RequestContext(request))
    return render(request,'app/perguntas.html', context)

#retorna Petições
def getDocPeticoes(request,IdDocPeticao,link):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'documenthistory/1/100/'+IdDocPeticao,0)
    jsonWorkflow = views.dicionaryWorkflow(request)

    context = {'documenthistory': XMLdata, 'workflow': jsonWorkflow, 'DocId': IdDocPeticao}
    #return render_to_response(link+'.html', context, context_instance=RequestContext(request))
    return render(request,'app/'+link+'.html', context)

#retorna Petições
def getDocInquerito(request,IdDocInquerito):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'documenthistory/1/100/'+IdDocInquerito,0)
    jsonWorkflow = views.dicionaryWorkflow(request)

    context = {'documenthistory': XMLdata, 'workflow': jsonWorkflow, 'DocId': IdDocInquerito}
    #return render_to_response('docInquerito.html', context, context_instance=RequestContext(request))
    return render(request,'app/docInquerito.html', context)

#retorna todas iniciativas
def getDocIniciativas(request,IdDocPeticao):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'documenthistory/1/100/'+IdDocPeticao,0)

    XMLdataY = menus.getCommittesMenu(request) #obtem dados do serviço getcommittes
    XMLmenusMinisterio = menus.getMinisteriesMenu(request)
    XMLGroupPolitico = menus.getGruposMenu(request)

    jsonWorkflow = views.dicionaryWorkflow(request)

    context = {'documenthistory': XMLdata, 'workflow': jsonWorkflow,'committes': XMLdataY, 'ministeries': XMLmenusMinisterio, 'grupoPolitico': XMLGroupPolitico, 'DocId': IdDocPeticao}

    #return render_to_response('docIniciativa.html', context, context_instance=RequestContext(request))
    return render(request,'app/docIniciativa.html', context)

#Retorna lista de Leis
def getLeis(request, IdLei):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'getdocsbytype/1/4/'+str(IdLei),0)
    #TotalLeis = tramites.getTotalTramites(request, IdLei)
    TotalLeis = getTotalTramites(request, IdLei)
    jsonWorkflow = views.dicionaryWorkflow(request)

    context = { 'feed':  XMLdata, 'TotalLeis': TotalLeis, 'workflow': jsonWorkflow}
    #return render_to_response('leis.html',context, context_instance=RequestContext(request))
    return render(request,'app/leis.html', context)

def getListLeis(request, IdLei):
    x               =   SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata         =   x.getContent(endereco+'getdocsbytype/1/4/'+str(IdLei),0)

    return HttpResponse(XMLdata)

#retorna lista de petições
def getPeticoes(request):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'getdocsbytype/1/4/'+str(3),0)
    #Totalpeticoes = tramites.getTotalTramites(request, str(3))
    Totalpeticoes = getTotalTramites(request, str(3))
    jsonWorkflow = views.dicionaryWorkflow(request)

    context = {'feed':  XMLdata, 'Totalpeticoes': Totalpeticoes, 'workflow': jsonWorkflow}

    #return render_to_response('peticoes.html',context, context_instance=RequestContext(request))
    return render(request,'app/peticoes.html', context)

#retorna lista de Inquerito
def getInquerito(request):
    x               =   SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata         =   x.getContent(endereco+'getdocsbytype/1/4/'+str(5),0)
    #Totalpeticoes = tramites.getTotalTramites(request, str(5))
    Totalpeticoes = getTotalTramites(request, str(5))
    jsonWorkflow = views.dicionaryWorkflow(request)

    context = {'feed':  XMLdata, 'Totalpeticoes': Totalpeticoes, 'workflow': jsonWorkflow}

    #return render_to_response('inquerito_parlamentar.html',context, context_instance=RequestContext(request))
    return render(request,'app/inquerito_parlamentar.html', context)

#retorna lista de interpelações
def getInterpelacoes(request):
    x               =   SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata         =   x.getContent(endereco+'getdocsbytype/1/4/'+str(4),0)
    #Totalpeticoes = tramites.getTotalTramites(request, str(4))
    Totalpeticoes = getTotalTramites(request, str(4))
    jsonWorkflow = views.dicionaryWorkflow(request)

    context = {'feed':  XMLdata, 'Totalpeticoes': Totalpeticoes, 'workflow': jsonWorkflow}

    #return render_to_response('interpelacoes.html',context, context_instance=RequestContext(request))
    return render(request,'app/interpelacoes.html', context)

#retorna lista de interpelações
def getDocInterpelacoes(request, IdDocInterpelacoes):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'documenthistory/1/100/'+IdDocInterpelacoes,4)
    jsonWorkflow = views.dicionaryWorkflow(request)

    context = {'documenthistory': XMLdata, 'workflow': jsonWorkflow, 'DocId': IdDocInterpelacoes}
    #return render_to_response('docInterpelacoes.html', context, context_instance=RequestContext(request))
    return render(request,'app/docInterpelacoes.html', context)

#retorna lista de iniciativas
def getIniciativa(request, IDMember):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    IDLegislatura = views.getCourentLegislature(request)
    XMLdata = x.getContent(endereco+'getdocsfromuser/1/10/'+str(IDLegislatura)+'/'+IDMember,0)
    XMLdataY = menus.getCommittesMenu(request) #obtem dados do serviço getcommittes
    XMLmenusMinisterio = menus.getMinisteriesMenu(request)
    XMLGroupPolitico = menus.getGruposMenu(request)


    #TotalIniciativa = tramites.getTotalIniciativa(request, IDLegislatura, IDMember)
    TotalIniciativa = getTotalIniciativa(request, IDLegislatura, IDMember)

    context = {'IDMember': IDMember, 'IDLegislatura': IDLegislatura, 'TotalIniciativa': TotalIniciativa, 'XMLdata': XMLdata, 'feed': '','committes': XMLdataY, 'ministeries': XMLmenusMinisterio, 'grupoPolitico': XMLGroupPolitico}
    #return render_to_response('Iniciativas.html',context, context_instance=RequestContext(request))
    return render(request,'app/Iniciativas.html', context)

#retorna lista de documentos associados
def getDocAssociados(request, IDDocumento, status):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'getdocsannex/1/100/'+IDDocumento,0)

    status = int(status)
    if status == 0:
        return HttpResponse(XMLdata)
    else:
        context = {'XMLdata': XMLdata}
        #return render_to_response('DocAssociado.html',context, context_instance=RequestContext(request))
        return render(request,'app/DocAssociado.html', context)
