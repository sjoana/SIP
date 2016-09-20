from app.server import server
from SILPCache import SILPCache

class menus(object):
    """description of class"""
    #gera Menus com dados das comiss�es
    def getCommittesMenu(request):
        y = SILPCache('cache')
        endereco = server.ServerEndereco(request)
        XMLdataY=y.getContent(endereco+'getcommittes/1/100',0)

        return XMLdataY

    #gera Menus com dados dos Minist�rios
    def getMinisteriesMenu(request):
        y = SILPCache('cache')
        endereco = server.ServerEndereco(request)
        XMLdataY=y.getContent(endereco+'getministeries/1/100',0)

        return XMLdataY

    #gera Menus com dados dos Grupos Pol�ticos
    def getGruposMenu(request):
        y = SILPCache('cache')
        endereco = server.ServerEndereco(request)
        XMLGroup=y.getContent(endereco+'getpoliticalgroups/1/100', 4)

        return XMLGroup

