"""
Definition of urls for FrontEnd.
"""

from datetime import datetime
from django.conf.urls import url
import django.contrib.auth.views

import app.forms
import app.views
import app.comissao
import app.deputado
import app.grupopolitico
import app.ministerio
import app.tramites

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = [
    url(r'^$', app.views.getHome),
    url(r'(?i)Deputados/', app.deputado.getMembers),
    url(r'(?i)DeputadosProcura/(?P<LimitInf>\d+)/(?P<LimitSup>\d+)/(?P<Name>.+)/(?P<partido>.+)/$', app.deputado.getMemberSearch),
    url(r'(?i)CountMember/(?P<Name>.+)/(?P<partido>.+)/$', app.deputado.getMemberSearchCount),
    url(r'(?i)Deputado/(?P<IDMember>\d+)/$', app.deputado.getMember), # retorna dados de um determinado deputado
    url(r'(?i)Governo/(?P<IDMember>\d+)/$', app.ministerio.getMember), # retorna dados de um determinado membro do governo
    url(r'(?i)User/(?P<IDMember>\d+)/$', app.deputado.getUser),
    url(r'(?i)DeputadoList/(?P<LimitInf>\d+)/(?P<LimitSup>\d+)/$', app.deputado.DeputadoList),
    url(r'(?i)DeputadoTotal/(?P<status>\d+)/$', app.deputado.getTotalNumberMember),

    url(r'(?i)Grupo_Politico/',app.grupopolitico.getListGP),
    url(r'(?i)Calendario/',app.views.getCalendar),
    url(r'(?i)Tramites/', app.tramites.getTramites),
    url(r'(?i)TramiteDoc/(?P<LimitInfI>\d+)/(?P<data>.+)/$',app.tramites.getDocTramite), #
    url(r'(?i)TramiteDocumento/(?P<LimitInfI>\d+)/(?P<datas>.+)/$',app.tramites.getTramitesDocumento), #

    url(r'(?i)Comissoes/(?P<IdCommittes>\d+)/$', app.comissao.getCommittesMembers),
    url(r'(?i)getcommitteemembers/(?P<LimitInfI>\d+)/(?P<LimitSup>\d+)/(?P<IdCommittes>\d+)/$', app.comissao.CommittesMemberList),

    url(r'(?i)Leis/(?P<IdLei>\d+)/$',app.tramites.getLeis),
    url(r'(?i)List/(?P<IdLei>\d+)/$',app.tramites.getListLeis), # url para ajax "faz listagem de tipo de Leis (proposta lei e projeto lei)"
    url(r'(?i)doclei/(?P<IdDocLei>\d+)/$', app.tramites.getDocLei),
    url(r'(?i)docLeiModal/(?P<IdDocLei>\d+)/$', app.tramites.getDocLeiModal),
    url(r'(?i)docPerguntaModal/(?P<IdDocPergunta>\d+)/$', app.tramites.docPerguntaModal),

    url(r'(?i)Ministerio/(?P<IdMinisterio>\d+)/$', app.ministerio.getMinisteries),
    url(r'(?i)GrupoPolitico/(?P<IdGpolitico>\d+)/$', app.grupopolitico.getGrupoPolitico),
    url(r'(?i)ListaMemberGrupo/(?P<LimitInfI>\d+)/(?P<NumberElements>\d+)/(?P<IdGroup>\d+)/$', app.grupopolitico.MemberGroupList),

    url(r'(?i)TPerguntas/$',app.tramites.getPerguntas),
    url(r'(?i)ListaT/(?P<LimitInf>\d+)/(?P<LimitSup>\d+)/(?P<IdTramite>\w+)$',app.tramites.getTramiteList),
    url(r'(?i)docperguntas/(?P<IdDocPergunta>\d+)/$', app.tramites.getDocPerguntas),

    url(r'(?i)Peticoes/$',app.tramites.getPeticoes),
    url(r'(?i)docpeticoes/(?P<IdDocPeticao>\d+)/(?P<link>\w+)/$', app.tramites.getDocPeticoes),

    url(r'(?i)Inquerito/$',app.tramites.getInquerito),

    url(r'(?i)Interpelacoes/$',app.tramites.getInterpelacoes),
    url(r'(?i)docInterpelacoes/(?P<IdDocInterpelacoes>\d+)/$', app.tramites.getDocInterpelacoes),

    url(r'(?i)Iniciativa/(?P<IDMember>\d+)$',app.tramites.getIniciativa),
    url(r'(?i)ListaAllTramite/(?P<LimitInf>\d+)/(?P<NumberElements>\d+)/(?P<IDLegislatura>\d+)/(?P<IDMember>\d+)/$',app.tramites.getAllTramiteList),
    url(r'(?i)docIniciativas/(?P<IdDocPeticao>\d+)/$', app.tramites.getDocIniciativas),

    url(r'(?i)docInquerito/(?P<IdDocInquerito>\d+)/$', app.tramites.getDocInquerito),

    url(r'(?i)Pesquisa_Avancada/$', app.views.getPesquisaAvancada),
    url(r'(?i)ResultadoPesquisa_Avancada/(?P<endpoint>\w+)/(?P<parametros>.+)/$', app.views.getResultadoPesquisaAvancada),

    url(r'(?i)Pesquisa/$', app.views.getPesquisa),
    #url(r'^docs/', include('rest_framework_swagger.urls')),
    url(r'(?i)printPDF/(?P<IdTramite>\w+)', app.views.printPDF),

    url(r'(?i)parlamentotl/', app.views.siteParlamento),
    url(r'(?i)parlamentocvCidadao/', app.views.siteParlamentoEspacoCidadao),

    url(r'(?i)DocumentoAssociado/(?P<IDDocumento>\d+)/(?P<status>\d+)/$', app.tramites.getDocAssociados),
]
