from app.server import server
from app.menus import menus
from django.shortcuts import render
from django.http import *
from django.template import RequestContext
from django.shortcuts import *
from django.core import serializers
from . import views
from SILPCache import SILPCache

"""description of class"""
def getMinisteries(request,IdMinisterio):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata =   x.getContent(endereco+'getministers/1/4/'+IdMinisterio,0)
    XMLdataY = menus.getCommittesMenu(request) #obtem dados do serviço getcommittes
    XMLMenuMinisterio = menus.getMinisteriesMenu(request)
    XMLGroupPolitico = menus.getGruposMenu(request)

    context = {'MinistersMembers': XMLdata, 'feed':  '', 'committes':  XMLdataY,'idMinisterio': IdMinisterio, 'ministeries': XMLMenuMinisterio, 'grupoPolitico': XMLGroupPolitico}
    #return render_to_response('Ministeries.html', context, context_instance=RequestContext(self))
    return render(request,'app/Ministeries.html', context)

def getMember(request,IDMember):
    x = SILPCache('cache')
    endereco = server.ServerEndereco(request)
    XMLdata = x.getContent(endereco+'getmembergov/'+IDMember,4)
    x.getImage(XMLdata)
    context = XMLdata

    return HttpResponse(context)

