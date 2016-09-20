import bottle
from bottle import static_file
import bottle_pgsql
import json
import psycopg2
from psycopg2.extensions import connection
from jinja2 import Template
#from weasyprint import HTML
import pdfkit

from django.core.serializers.json import DjangoJSONEncoder
from DatabaseConfigurations import Configs
import base64
import time
from time import mktime
from fpdf import FPDF, HTMLMixin
from datetime import datetime


app = bottle.Bottle()
configuration = Configs.Config('configuracoes.cfg')
plugin = bottle_pgsql.Plugin('host=192.168.160.120 '+
    'dbname=' + configuration.connStringDB() + ' user=' + configuration.connStringUser() + ' password=' + configuration.connStringPassword())
app.install(plugin)
conn = psycopg2.connect('dbname=' + configuration.connStringDB() + ' user=' + configuration.connStringUser() + ' host=' + configuration.connStringHost() +  ' password=' + configuration.connStringPassword())


@app.route('/docs/<filename:re:.*>')
def html(filename):
    return static_file(filename, root='../')


@app.error(404)
def error404(error):
    return '<h1>Página inexistente</h1>'


@app.error(500)
def error500(error):
    return '<h1>Erro de servidor interno</h1>'


@app.route('/getmembers/<start>/<offset>')
def members(db, start, offset):
    """
    Retorna o conjunto de membros da actual legislatura do SILP (Bungeni)
    """
    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset) -1
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = 'select * from public.getMembers(%s,%s);'
    db.execute(query, (start, end))
    resultados = db.fetchall()
    for i, val in enumerate(resultados):
        for j, value in enumerate(val):
            if value == 'user_image':
                if resultados[i]["user_image"] == None:
                    resultados[i]['user_image'] = 'None'
                else:
                    wb = open("C:/tmp/cache/members/" + resultados[i]['user_email'], 'wb')
                    wb.write(resultados[i]['user_image'])
                    wb.close()
                    resultados[i]['user_image'] = resultados[i]['user_email']
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson




@app.route('/getmembersearch/<start>/<offset>/<nome>/<party>')
def memberssearch(db,start, offset, nome,party):
    """
    Retorna o conjunto de membros da actual legislatura do SILP (Bungeni)
    """

    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"


    if (party=='0'):
        party='';

    if (nome=='0'):
        nome='';


    party='%'+party+'%'
    nome = '%'+nome+'%'
    nome = nome.replace(" ","%")
    party = party.lower()
    query = 'select * from public.getMembersPesquisaParty(%s,%s,%s,%s);'
    db.execute(query, (start,end,nome,party))
    resultados = db.fetchall()
    for i, val in enumerate(resultados):
        for j, value in enumerate(val):
            if value == 'user_image':
                if resultados[i]["user_image"] == None:
                    resultados[i]['user_image'] = 'None'
                else:
                    wb = open("C:/tmp/cache/members/" + resultados[i]['user_email'], 'wb')
                    wb.write(resultados[i]['user_image'])
                    wb.close()
                    resultados[i]['user_image'] = resultados[i]['user_email']
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson



@app.route('/getmemberImage/<idM>')
def getmemberImage(db, idM):
    query = 'select * from public.getuser(%s,%s)'
    db.execute(query, (idM, 0))
    resultados = db.fetchall()
    for i, val in enumerate(resultados):
        for j, value in enumerate(val):
             if value == 'user_image':
                if resultados[i]["user_image"] == None:
                    resultados[i]['user_image'] = 'None'
                else:
                    wb = open("C:/tmp/cache/members/" + resultados[i]['user_email'], 'wb')
                    wb.write(resultados[i]['user_image'])
                    wb.close()
                    resultados[i]['user_image'] = resultados[i]['user_image']  
    #resultadosJson = json.dumps(resultados['user_image'], cls=DjangoJSONEncoder)
    return resultados[0]['user_image']


@app.route('/getdocsearch/<start>/<offset>/<title>/<text>/<owner>')
def getdocsearch(db,start, offset, title,text, owner):


    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"


    if (title=='0'):
        title=''
    else:
        title='%'+title+'%'

    if (text=='0'):
        text=''
    else:
        text = '%'+text+'%'


    if (owner=='0'):
        owner=''
    else:
        owner = '%'+owner+'%'
        owner = owner.replace(" ","%")







    query = 'select * from public.getDocsPesquisa(%s,%s,%s,%s,%s);'
    db.execute(query, (start,end,title,text,owner))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson




@app.route('/getcommitteesearch/<start>/<offset>/<searchName>/<documents>/<searchCommittee>')
def getcommsearch(db,start, offset, searchName,documents, searchCommittee):


    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"


    if (searchName=='0'):
        searchName=''
    else:
        searchName='%'+searchName+'%'
        searchName = searchName.replace(" ","%")

    if (documents=='0'):
        documents=''
    else:
        documents = '%'+documents+'%'


    if (searchCommittee=='0'):
        searchCommittee=''
    else:
        searchCommittee = '%'+searchCommittee+'%'



    query = 'select * from public.getpesquisacommittee(%s,%s,%s,%s,%s);'
    db.execute(query, (start,end,searchName,documents,searchCommittee))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson



@app.route('/getpoliticalgroupsearch/<start>/<offset>/<searchName>/<documents>/<searchCommittee>')
def getcommsearch(db,start, offset, searchName,documents, searchCommittee):


    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"


    if (searchName=='0'):
        searchName=''
    else:
        searchName='%'+searchName+'%'
        searchName = searchName.replace(" ","%")

    if (documents=='0'):
        documents=''
    else:
        documents = '%'+documents+'%'


    if (searchCommittee=='0'):
        searchCommittee=''
    else:
        searchCommittee = '%'+searchCommittee+'%'



    query = 'select * from public.getPesquisaPoliticalGroup(%s,%s,%s,%s,%s);'
    db.execute(query, (start,end,searchName,documents,searchCommittee))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson










@app.route('/getcompletesearch/<start>/<offset>/<searchParameter>')
def getcommsearch(db,start, offset, searchParameter):


    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"


    if (searchParameter=='0'):
        searchParameter=''
    else:
        searchParameter='%'+searchParameter+'%'



    resultadosJson = []
    for i in range(3):
        resultadosJson.append(1)


    query = 'select * from public.getPesquisaPoliticalGroup(%s,%s,%s,%s,%s);'
    db.execute(query, (start,end,searchParameter,searchParameter,searchParameter))
    resultados = db.fetchall()
    resultadosJson[0] = json.dumps(resultados, cls=DjangoJSONEncoder)


    query = 'select * from public.getdocspesquisa(%s,%s,%s,%s,%s);'
    db.execute(query, (start,end,searchParameter,searchParameter,searchParameter))
    resultados = db.fetchall()
    resultadosJson[1] = json.dumps(resultados, cls=DjangoJSONEncoder)



    query = 'select * from public.getPesquisacommittee(%s,%s,%s,%s,%s);'
    db.execute(query, (start,end,searchParameter,searchParameter,searchParameter))
    resultados = db.fetchall()
    resultadosJson[2] = json.dumps(resultados, cls=DjangoJSONEncoder)



    return resultadosJson










@app.route('/getmembersearch/<start>/<offset>/<nome>/')
def memberssearch(db,start, offset, nome):
    """
    Retorna o conjunto de membros da actual legislatura do SILP (Bungeni)
    """


    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"


    nome = '%'+nome+'%'
    nome = nome.replace(" ","%")
    query = 'select * from public.getMembersPesquisaParty(%s,%s,%s);'
    db.execute(query, (start,end,nome))
    resultados = db.fetchall()
    for i, val in enumerate(resultados):
        for j, value in enumerate(val):
            if value == 'user_image':
                if resultados[i]["user_image"] == None:
                    resultados[i]['user_image'] = 'None'
                else:
                    wb = open("C:/tmp/cache/members/" + resultados[i]['user_email'], 'wb')
                    wb.write(resultados[i]['user_image'])
                    wb.close()
                    resultados[i]['user_image'] = resultados[i]['user_email']
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson



@app.route('/getpartys')
def memberscount(db):
    query = 'select * from public.getPartys();'
    db.execute(query)
    resultados = db.fetchall()
    for i, val in enumerate(resultados):
        if resultados[i]["party_name"] == None:
            resultados[i]['party_name'] = 'None'
        resultados[i]["party_name"] = resultados[i]["party_name"].upper()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson



@app.route('/getmembersearchcount/<nome>/<party>')
def memberssearch(db, nome,party):
    """
    Retorna o conjunto de membros da actual legislatura do SILP (Bungeni)
    """


    if (party=='0'):
        party='';

    if (nome=='0'):
        nome='';


    party='%'+party+'%'
    nome = '%'+nome+'%'
    nome = nome.replace(" ","%")
    party = party.lower()
    query = 'select * from public.getMembersPesquisaPartyCount(%s,%s);'
    db.execute(query, (nome,party))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson





@app.route('/getmemberscount')
def memberscount(db):
    query = 'select * from public.getMemberscount();'
    db.execute(query)
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/getministerscount/<id>')
def ministerscount(db, id):
    query = 'select * from public.getMinisterscount(%s,%s);'
    db.execute(query, (0, id))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/getpoliticalgroupmemberscount/<id>')
def politicalmemberscount(db, id):
    query = 'select * from public.getpoliticalmemberscount(%s,%s);'
    db.execute(query, (0, id))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/getcommitteememberscount/<id>')
def getcommitteememberscount(db, id):
    query = 'select * from public.getcommitteememberscount(%s,%s);'
    db.execute(query, (0, id))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson

@app.route('/getscheduleditemscount/<startdate>/<enddate>')
def getcommitteememberscount(db, startdate,enddate):
    query = "select * from public.getscheduleditemscount(to_date(%s, 'DD-MM-YYYY'), to_date(%s, 'DD-MM-YYYY'));"
    db.execute(query, (startdate, enddate))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/documentstypecount/<docType>')
def projleicount(db,docType):
    query = 'Select * from public.documentstypecount(%s,%s)'
    db.execute(query, (0,docType))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson



@app.route('/getcommitteemembers/<start>/<offset>/<id>')
def politicalgroupmembers(db, start, offset, id):
    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset) - 1
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = 'Select * from public.getcommitteemembers(%s, %s, %s);'
    db.execute(query, (start, end, id))
    resultados = db.fetchall()
    for i, val in enumerate(resultados):
        for j, value in enumerate(val):
            if value == 'user_image':
                if resultados[i]["user_image"] == None:
                    resultados[i]['user_image'] = 'None'
                else:
                    wb = open("C:/tmp/cache/members/" + resultados[i]['user_email'], 'wb')
                    wb.write(resultados[i]['user_image'])
                    wb.close()
                    resultados[i]['user_image'] = resultados[i]['user_email']
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/getpoliticalgroupmembers/<start>/<offset>/<id>')
def getpoliticalgroupmembers(db, start, offset, id):
    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset) -1
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = 'Select * from public.getpoliticalgroupmembers(%s, %s, %s);'
    db.execute(query, (start, end, id))
    resultados = db.fetchall()
    for i, val in enumerate(resultados):
        for j, value in enumerate(val):
            if value == 'user_image':
                if resultados[i]["user_image"] == None:
                    resultados[i]['user_image'] = 'None'
                else:
                    wb = open("C:/tmp/cache/members/" + resultados[i]['user_email'], 'wb')
                    wb.write(resultados[i]['user_image'])
                    wb.close()
                    resultados[i]['user_image'] = resultados[i]['user_email']
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/getgovernmentmembers/<start>/<offset>')
def governmentmembers(db, start, offset):
    query = 'select * from public.getgovernmentmembers(%s,%s)'

    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = 'Select * from public.getgovernmentmembers(%s, %s);'
    db.execute(query, (start, end))
    resultados = db.fetchall()
    for i, val in enumerate(resultados):
        for j, value in enumerate(val):
            if value == 'user_image':
                if resultados[i]["user_image"] == None:
                    resultados[i]['user_image'] = 'None'
                else:
                    wb = open("C:/tmp/cache/members/" + resultados[i]['user_email'], 'wb')
                    wb.write(resultados[i]['user_image'])
                    wb.close()
                    resultados[i]['user_image'] = resultados[i]['user_email']
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/getlegislaturehistoricmembers/<start>/<offset>/<chamberId>')
def getlegislaturehistoricmembers(db, start, offset, chamberId):
    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0 or int(chamberId) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = 'Select * from public.getlegislatureshistoricmembers(%s, %s, %s);'
    db.execute(query, (start, end, chamberId))
    resultados = db.fetchall()
    for i, val in enumerate(resultados):
        for j, value in enumerate(val):
            if value == 'user_image':
                if resultados[i]["user_image"] == None:
                    resultados[i]['user_image'] = 'None'
                else:
                    wb = open("C:/tmp/cache/members/" + resultados[i]['user_email'], 'wb')
                    wb.write(resultados[i]['user_image'])
                    wb.close()
                    resultados[i]['user_image'] = resultados[i]['user_email']
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/getlegislatures/<start>/<offset>')
def getlegislatures(db, start, offset):
    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = 'Select * from public.getlegislatures(%s,%s)'
    db.execute(query, (start, end))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/getpoliticalgroups/<start>/<offset>')
def getpoliticalgroups(db, start, offset):
    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = 'Select * from public.getpoliticalgroups(%s,%s)'
    db.execute(query, (start, end))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson

@app.route('/getgroup/<idGroup>')
def getgroupsi(db, idGroup):
    try:
        if int(idGroup) < 1 :
            raise Exception
    except Exception:
        return "<h1>Parametros inválidos</h1>"
    query = 'Select * from public.getgroup(%s)'
    db.execute(query, (idGroup,))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson

@app.route('/getcommittes/<start>/<offset>')
def getcommittes(db, start, offset):
    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = 'Select * from public.getcommittes(%s,%s)'
    db.execute(query, (start, end))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/getpoliticalgroups/<start>/<offset>')
def getpoliticalgroups(db, start, offset):
    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = 'Select * from public.getpoliticalgroups(%s,%s)'
    db.execute(query, (start, end))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/getministeries/<start>/<offset>')
def getministrys(db, start, offset):
    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = 'Select * from public.getministeries(%s,%s)'
    db.execute(query, (start, end))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/getactivelegislature/<start>/<offset>')
def getactivelegislature(db, start, offset):
    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = 'Select * from public.getactivelegislature(%s,%s)'
    db.execute(query, (start, end))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/documenthistory/<start>/<offset>/<docid>')
def documenthistory(db, start, offset, docid):
    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0 or int(docid) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = 'Select * from public.documenthistory(%s,%s,%s)'
    db.execute(query, (start, end, docid))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/getdocsbytype/<start>/<offset>/<docType>')
def getdocsbytype(db, start, offset, docType):
    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0 :
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = 'Select * from public.getdocsbytype(%s,%s,%s)'
    db.execute(query, (start, end, docType))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson




@app.route('/getdocsannex/<start>/<offset>/<docId>')
def getdocsannex(db, start, offset, docId):
    aux = -1
    end = ''

    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = 'Select * from public.getdocsannex(%s,%s,%s)'
    db.execute(query, (start, end, docId))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson

@app.route('/getdocsannexedfiles/<start>/<offset>/<docId>')
def getdocsannex(db, start, offset, docId):
    aux = -1
    end = ''

    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
         return "<h1>Parametros inválidos</h1>"

    #a = connection.lobject(conn,oid=0e165c14b41d9983d7bfb8d80580116a)
    query = 'Select * from public.getdocsannexedfiles(%s,%s,%s)'
    db.execute(query, (start, end, docId))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/getscheduleditems/<start>/<offset>')
def getministeries(db, start, offset):
    aux = -1
    end = ''
    startdate = '01-01-0000'
    enddate = '01-01-3000'
    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = "Select * from public.getscheduleditems(%s,%s,to_date(%s, 'DD-MM-YYYY'), to_date(%s, 'DD-MM-YYYY'))"
    db.execute(query, (start, end, startdate, enddate))
    resultados = db.fetchall()
    for i, val in enumerate(resultados):
        for j, value in enumerate(val):
            if value == 'sittingstart_date':
                resultados[i]['sittingstart_date'] = int(
                    mktime((resultados[i]['sittingstart_date']).timetuple()) * 1000)
            if value == 'sittingend_date':
                resultados[i]['sittingend_date'] = int(mktime((resultados[i]['sittingend_date']).timetuple()) * 1000)
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/getscheduleditems/<start>/<offset>/<startdate>/<enddate>')
def getscheditems(db, start, offset, startdate, enddate):
    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = "Select * from public.getscheduleditems(%s,%s,to_date(%s, 'DD-MM-YYYY'), to_date(%s, 'DD-MM-YYYY'))"
    db.execute(query, (start, end, startdate, enddate))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/sessionsittings/<start>/<offset>/<chamberId>/<sessionId>')
def sessionsittings(db, start, offset, chamberId, sessionId):
    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset)
        if (int(start) < 1 or int(offset) < 0) or (int(chamberId) < 0 or int(sessionId) < 0):
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = 'Select * from public.sessionsittings(%s,%s,%s,%s)'
    db.execute(query, (start, end, chamberId, sessionId))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/groupsittings/<start>/<offset>/<groupId>/<startdate>/<enddate>')
def groupsittings(db, start, offset, groupId, startdate, enddate):
    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset)
        if (int(start) < 1 or int(offset) < 0) or (int(groupId) < 0 ):
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = "Select * from public.groupsittings(%s,%s,%s,to_date(%s, 'DD-MM-YYYY'), to_date(%s, 'DD-MM-YYYY'));"
    db.execute(query, (start, end, groupId, startdate, enddate))
    resultados = db.fetchall()

    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/groupsittings/<start>/<offset>/<groupId>')
def groupsittings(db, start, offset, groupId):
    aux = -1
    end = ''
    startdate = '01-01-0000'
    enddate = '01-01-3000'
    try:
        aux = int(start) + int(offset)
        if (int(start) < 1 or int(offset) < 0) or (int(groupId) < 0 ):
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = "Select * from public.groupsittings(%s,%s,%s,to_date(%s, 'DD-MM-YYYY'), to_date(%s, 'DD-MM-YYYY'));"
    db.execute(query, (start, end, groupId, startdate, enddate))
    resultados = db.fetchall()
    for i, val in enumerate(resultados):
        for j, value in enumerate(val):
            if value == 'sittingstart_date':
                resultados[i]['sittingstart_date'] = int(
                    mktime((resultados[i]['sittingstart_date']).timetuple()) * 1000)
            if value == 'sittingend_date':
                resultados[i]['sittingend_date'] = int(mktime((resultados[i]['sittingend_date']).timetuple()) * 1000)

    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/getdocsfromuser/<start>/<offset>/<chamberId>/<userId>')
def getdocsfromuser(db, start, offset, chamberId, userId):
    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset) -1
        if (int(start) < 1 or int(offset) < 0) or (int(chamberId) < 0 or int(userId) < 0):
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = 'Select * from public.getdocsfromuser(%s,%s,%s,%s)'
    db.execute(query, (start, end, chamberId, userId))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/getdocsfromusercount/<chamberId>/<userId>')
def getdocsfromusercount(db,  chamberId, userId):
    aux = -1
    end = ''


    query = 'Select * from public.getdocsfromusercount(%s,%s)'
    db.execute(query, ( chamberId, userId))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/getministers/<start>/<offset>/<id>')
def getministers(db, start, offset, id):
    aux = -1
    end = ''
    try:
        aux = int(start) + int(offset)
        if int(start) < 1 or int(offset) < 0:
            raise Exception
        end = str(aux)
    except Exception:
        return "<h1>Parametros inválidos</h1>"

    query = 'Select * from public.getMinisters(%s,%s,%s)'
    db.execute(query, (start, end, id))
    resultados = db.fetchall()
    for i, val in enumerate(resultados):
        for j, value in enumerate(val):
            if value == 'user_image':
                if resultados[i]["user_image"] == None:
                    resultados[i]['user_image'] = 'None'
                else:
                    wb = open("C:/tmp/cache/members/" + resultados[i]['user_email'], 'wb')
                    wb.write(resultados[i]['user_image'])
                    wb.close()
                    resultados[i]['user_image'] = resultados[i]['user_email']
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/getmembergov/<idM>')
def getmembergov(db, idM):
    """
    Retorna um membro do governo da legislatura atual
    """

    query = 'select * from public.getMember(%s,%s)'
    db.execute(query, (idM,'bungeni.MinistryMember'))
    resultados = db.fetchall()
    for i, val in enumerate(resultados):
        for j, value in enumerate(val):
            if value == 'user_image':
                if resultados[i]["user_image"] == None:
                    resultados[i]['user_image'] = 'None'
                else:
                    wb = open("C:/tmp/cache/members/" + resultados[i]['user_email'], 'wb')
                    wb.write(resultados[i]['user_image'])
                    wb.close()
                    resultados[i]['user_image'] = resultados[i]['user_email']
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson

@app.route('/getmember/<idM>')
def getmember(db, idM):
    """
    Retorna o conjunto de membros da actual legislatura do SILP (Bungeni)
    """

    query = 'select * from public.getMember(%s,%s)'
    db.execute(query, (idM, 'bungeni.MemberAssembly'))
    resultados = db.fetchall()
    for i, val in enumerate(resultados):
        for j, value in enumerate(val):
            if value == 'user_image':
                if resultados[i]["user_image"] == None:
                    resultados[i]['user_image'] = 'None'
                else:
                    wb = open("C:/tmp/cache/members/" + resultados[i]['user_email'], 'wb')
                    wb.write(resultados[i]['user_image'])
                    wb.close()
                    resultados[i]['user_image'] = resultados[i]['user_email']
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/getuser/<idM>')
def getuser(db, idM):
    query = 'select * from public.getuser(%s,%s)'
    db.execute(query, (idM, 0))
    resultados = db.fetchall()
    for i, val in enumerate(resultados):
        for j, value in enumerate(val):
            if value == 'user_image':
                if resultados[i]["user_image"] == None:
                    resultados[i]['user_image'] = 'None'
                else:
                    wb = open("C:/tmp/cache/members/" + resultados[i]['user_email'], 'wb')
                    wb.write(resultados[i]['user_image'])
                    wb.close()
                    resultados[i]['user_image'] = resultados[i]['user_email']
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)
    return resultadosJson


@app.route('/getimage/<image>')
def getimage(image):
    return static_file(image, root='../images/')


@app.route('/getdoc/<guid>')
def getidoc(guid):
    return static_file(guid, root='/opt/bungeni/bungeni_apps/bungeni/fs/',download=True)


def htmlparser(txt):
    htmlcodes = ['&Aacute;', '&aacute;', '&Agrave;', '&Acirc;', '&agrave;', '&Acirc;', '&acirc;', '&Auml;', '&auml;', '&Atilde;', '&atilde;', '&Aring;', '&aring;', '&Aelig;', '&aelig;', '&Ccedil;', '&ccedil;', '&Eth;', '&eth;', '&Eacute;', '&eacute;', '&Egrave;', '&egrave;', '&Ecirc;', '&ecirc;', '&Euml;', '&euml;', '&Iacute;', '&iacute;', '&Igrave;', '&igrave;', '&Icirc;', '&icirc;', '&Iuml;', '&iuml;', '&Ntilde;', '&ntilde;', '&Oacute;', '&oacute;', '&Ograve;', '&ograve;', '&Ocirc;', '&ocirc;', '&Ouml;', '&ouml;', '&Otilde;', '&otilde;', '&Oslash;', '&oslash;', '&szlig;', '&Thorn;', '&thorn;', '&Uacute;', '&uacute;', '&Ugrave;', '&ugrave;', '&Ucirc;', '&ucirc;', '&Uuml;', '&uuml;', '&Yacute;', '&yacute;', '&yuml;', '&copy;', '&reg;', '&trade;', '&euro;', '&cent;', '&pound;', '&lsquo;', '&rsquo;', '&ldquo;', '&rdquo;', '&laquo;', '&raquo;', '&mdash;', '&ndash;', '&deg;', '&plusmn;', '&frac14;', '&frac12;', '&frac34;', '&times;', '&divide;', '&alpha;', '&beta;', '&infin']
    funnychars = ['\xc1','\xe1','\xc0','\xc2','\xe0','\xc2','\xe2','\xc4','\xe4','\xc3','\xe3','\xc5','\xe5','\xc6','\xe6','\xc7','\xe7','\xd0','\xf0','\xc9','\xe9','\xc8','\xe8','\xca','\xea','\xcb','\xeb','\xcd','\xed','\xcc','\xec','\xce','\xee','\xcf','\xef','\xd1','\xf1','\xd3','\xf3','\xd2','\xf2','\xd4','\xf4','\xd6','\xf6','\xd5','\xf5','\xd8','\xf8','\xdf','\xde','\xfe','\xda','\xfa','\xd9','\xf9','\xdb','\xfb','\xdc','\xfc','\xdd','\xfd','\xff','\xa9','\xae','\u2122','\u20ac','\xa2','\xa3','\u2018','\u2019','\u201c','\u201d','\xab','\xbb','\u2014','\u2013','\xb0','\xb1','\xbc','\xbd','\xbe','\xd7','\xf7','\u03b1','\u03b2','\u221e']
    #filename = raw_input("Write the full name of the file you wish to fix: \n")
    #filetext = open(filename,  'r')
    #textcontent = filetext.read()
    newtext = ''
    for char in txt:
        if char not in funnychars:
            newtext = newtext + char
        else:
            newtext  = newtext + htmlcodes[funnychars.index(char)]
    #resultfile = open('result.txt', 'w')
    #resultfile.write(newtext)
    #resultfile.close()
    #filetext.close()
    return newtext

@app.route('/document2pdf/<docid>')
def documenthistory(db, docid):



    html_string = ''


    aux = -1
    end = ''


    query = 'Select * from public.documenthistory(%s,%s,%s)'
    db.execute(query, (1, 100, docid))
    resultados = db.fetchall()
    resultadosJson = json.dumps(resultados, cls=DjangoJSONEncoder)

    text = json.loads(resultadosJson)
    texto = text[0]["docbody"]
    #teste =  texto.encode('latin-1', 'xmlcharrefreplace')

    image = open('parlamento-de-timor.jpg','rb')
    img= base64.b64encode(image.read())

    html_template = open('html_model.html',"r")


    template = Template(html_template.read())
    #b = template.render(titulo=text[0]["doctitle"], texto=text[0]["docbody"],image=img.decode(encoding='utf-8'))
    b = template.render(titulo=text[0]["doctitle"], texto=texto, image=img.decode(encoding='utf-8'))

   
    css = 'teste.css'
    #config = pdfkit.configuration(wkhtmltopdf='C:/tmp/wkhtmltopdf/bin/wkhtmltopdf.exe')
    html_template_and_content = pdfkit.from_string(b, "doc.pdf", css= css)

    #html_template_and_content = HTML(string=b)
    #html_template_and_content.write_pdf('doc.pdf',stylesheets={'teste.css'})



    #return html_template_and_content
    return static_file("doc.pdf", root='')



app.run(host='localhost', port=8089)
