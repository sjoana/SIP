/**
 * Created by emanuel on 1/16/15.
 */

function alterFormatData(data) {
    var novoData = data.split('-');
    return novoData[2] + '-' + novoData[1] + '-' + novoData[0];
}

$(function () {
    var tabela = $('.table').dataTable({
        "bFilter": false,
        "bLengthChange": false,
        "ordering": false,
        "bPaginate": false,
        "bInfo": false
    });

    //Cria menu de comissões automáticamente
    var tamCommittes = $(XmlCommittes).find('item').length;
    var menuCommittes = $('#comissoes');

    menuCommittes.empty();

    for (i = 0; i < tamCommittes; i++) {
        var DescCommittes = $($($(XmlCommittes).find('item')[i]).find('group_full_name')).text();
        var IdCommittes = $($($(XmlCommittes).find('item')[i]).find('group_id')).text();

        menuCommittes.append(' <li id=' + IdCommittes + 'Com> <a href="/Comissoes/' + IdCommittes + '">' + DescCommittes + '</a> </li>');
    }

    //Cria menu de ministérios automáticamente
    var tamMinisterio = $(XmlMinisterio).find('item').length;
    var menuMinisterio = $('#ministerios');

    menuMinisterio.empty();

    for (i = 0; i < tamMinisterio; i++) {
        var DescMinisterio = $($($(XmlMinisterio).find('item')[i]).find('group_full_name')).text();
        var IdMinisterio = $($($(XmlMinisterio).find('item')[i]).find('group_id')).text();
        //hardcoded
        menuMinisterio.append(' <li id=' + IdMinisterio + 'Min> <a href="/Ministerio/' + IdMinisterio + '">' + DescMinisterio + '</a> </li>');
    }

    //Cria menu de grupos políticos automáticamente
    var tamGruposPolitico = $(XmlGruposPoliticos).find('item').length;
    var menuGruposPolitico = $('#gruposPoliticos');

    menuGruposPolitico.empty();

    for (i = 0; i < tamGruposPolitico; i++) {
        var DescGruposP = $($($(XmlGruposPoliticos).find('item')[i]).find('group_full_name')).text();
        var IdGruposPoliticos = $($($(XmlGruposPoliticos).find('item')[i]).find('group_id')).text();
        //hardcoded
        menuGruposPolitico.append(' <li id=' + IdGruposPoliticos + 'Grop> <a href="/GrupoPolitico/' + IdGruposPoliticos + '">' + DescGruposP + '</a> </li>');
    }
});

// faz preenchimento de feed
$(function () {
    var div_feed = $('.content_feed');
    if (typeof xml_feed === 'undefined') {
        return;
    }
    
    var tam = $(xml_feed).find('title').length;
    if (tam > 6)
        tam = 6;
    for (x = 0; x < tam; x++) {
        var newsTitle = $($($(xml_feed).find('item')[x]).find('title')[0]).text();
        var newsImage = $($($(xml_feed).find('item')[x]).find('enclosure')[0]).attr('url');
        var newsDate = $($($(xml_feed).find('item')[x]).find('pubDate')[0]).text();
        var linkNews = $($($(xml_feed).find('item')[x]).find('link'))[0].nextSibling.data;
        var sourceUrl = $($($(xml_feed).find('item')[x]).find('source')[0]).attr('url');
        newsDate = newsDate.split("Z");
        newsDate = new Date(Date.parse(newsDate[0]));

        if (newsImage == null) newsImage = '/static/app/image/noImage.jpg';

        div_feed.append(
		'<div class="row">' +
			'<div class="col-xs-3" id="imagemContent"><img src="' + newsImage + '" class="newsradio img-thumbnail" /></div>' +
			'<div class="col-xs-9" id="newsTitle">' +
			'<p><a class="title" data-link-news="' + linkNews + '">' + newsTitle + '</a></p>' +
			'<p class="small"><i class="fa fa-calendar-o" aria-hidden="true"></i> ' + newsDate.getDate() + '/' + newsDate.getMonth() + '/' + newsDate.getFullYear() + '<br/>' +
			'<i class="fa fa-external-link" aria-hidden="true"></i> <a href="' + linkNews + '">' + sourceUrl + '</a></p>' +
			'</div><div class="clearfix"></div>' +
		'</div>');

    }
    $('.title').click(function () {
        $('#modaltitle').text($(this).text());
        title = $(this).text();
        link = $(this).attr('data-link-news');
        var headerImage = $($($(xml_feed).find('title:contains(' + title + ')').parent()).find('enclosure')[0]).attr('url');
        contents = $($($(xml_feed).find('title:contains(' + title + ')').parent()).find('long')[0]).text();
        contents += '<hr/><i class="fa fa-external-link"></i> <a href="' + link + '" target="_blank" class="small">Ver no site</a>';
        //if (headerImage != null)
        //    contents = '<img id="newsFoto" src="' + headerImage + '" alt="foto" />' + contents;
        $('#modalnews').html(contents);
        $('#noticia').modal('show');
    }
	);
});

$(window).scroll(function () {
    if ($(window).scrollTop() > 88) {
        $('.scroller').addClass('stuck');
    } else {
        $('.scroller').removeClass('stuck');
    }
});

function alterafocusmenu(idMenu, idSubmenu, tipoMenu) {
    //altera icone do menu silp para ativo ou inativo
    //var home = $('.botton-silp');
    //if(idMenu != 'home'){
    //    home.attr('src','/../staticpub/image/boton_silp-1.png');
    //}else{
    //    home.attr('src','/../staticpub/image/boton_silp-1.png');
    //}

    $('#' + idMenu).removeClass('init-arrow-down');

    var menu = '#' + idMenu;
    var submenu = '#' + idSubmenu;

    if (tipoMenu != 'tramite') {
        if (idMenu == 'agenda' || idMenu == 'acerca' || idMenu == 'home' || idMenu == 'deputado') {
            $(menu).addClass('init-arrow active');
        } else {
            $(menu).addClass('arrow-up active');
            $(menu + ' ul').css('display', 'block');
            $(menu + ' ul ' + submenu).addClass('active');
        }
    } else {
        $(menu).addClass('init-arrow active');
    }
}

$(function () {
    $('.dropdown-menu li').click(function () {
        var obj = $(this).text();
    });
});


/*Faz Listagem de membros*/
function showmembres(xml, context) {
    tam = $(xml).find('item').length;
    div_html = $('.commentlist');
    msn = ''

    if (tam == 0) {
        msn = '<p class="semRegisto">Sem registo</p>';
        div_html.append(msn);
    }

    for (i = 0; i < tam; i++) {
        var member = $(xml).find('item')[i]
        var nome = $($(member).find('user_first_name')).text();
        var middle_name = $($(member).find('user_middle_name')).text();
        var last_name = $($(member).find('user_last_name')).text();
        var desc_user = $($(member).find('user_description')).text();
        var image_user = $($(member).find('user_image')).text();
        var IdMember = $($(member).find('user_id')).text();
        var gender = $($(member).find('user_gender')).text();
        if (image_user == 'None')
            image_user = "/static/app/image/nophoto" + gender + '.jpg';
        else
            image_user = "http://localhost:8089/getmemberImage/" + IdMember;
        if (desc_user == "")
            desc_user = '[Sem informação disponível para esta secção.]';
        div_html.append('<div class="col-lg-4 col-xs-12">'+
            '<div class="panel panel-default">' +
                '<div class="panel-heading">' +
                     '<h5 style="height:34px;"><a href="#" onclick="showDetaisMembrer(' + IdMember +",'"+context + "')\">" + nome.trim() + " " + middle_name.trim() + " " + last_name.trim() + '</a></h5>' +
                '</div>' +
                '<div class="panel-body">' +
                    '<div class="text-center"><a href="#"  onclick="showDetaisMembrer(' + IdMember +",'"+context + '\')"><img style="height:150px;" src="' + image_user + '" alt="' + nome.trim() + " " + middle_name.trim() + " " + last_name.trim() + '" class="img-thumbnail" /></a></div>' +
                '</div>' +
            '</div>' +
        '</div>');
    }
    $('article').readmore({
        speed: 500,
        collapsedHeight: 70
    });
    return div_html;
}

//função que apresenta dados acerca de um determinado Utilizador no modal (recebe o id do utilizador)
function showDetaisMembrer(id, context) {
    // show popup com dados do deputado
    var IdMember = id;
    $.ajax({
        url: "/" + context + "/" + id,
        success: function (data) {
            var v_name = $($($(data)).find('user_first_name')).text();
            var v_middle_name = $($($(data)).find('user_middle_name')).text();
            var v_last_name = $($($(data)).find('user_last_name')).text();
            var image_user = $($($(data)).find('user_image')).text();
            var data_inicio = $($($(data)).find('member_start_date')).text();
            var desc_user = $($($(data)).find('member_notes')).text();
            var gender = $($($(data)).find('user_gender')).text();
            if (image_user == 'None' || image_user == '')
                image_user = "/static/app/image/nophoto" + gender + '.jpg';
            else
                image_user = "http://localhost:8089/getmemberImage/" + IdMember;
            /* var mail  = $($($(data)).find('user_email')).text(); */
            $('#myModalLabel').html('<h3>' + v_name.trim() + " " + v_middle_name.trim() + " " + v_last_name.trim() + '</h3>')
            $('.modal-body').html('<div class="col-xs-4"><img class="img-thumbnail" src="'+ image_user + '"></div>' +
            '<div class="col-xs-8 conteudoInfo">' +
           /* 'Partido: <br>'+ */
            '<b>Data de empossamento</b>: ' + alterFormatData(data_inicio) + '</br>' +
          /*  '<span>Email: <i class="mail">'+mail+'</i></span><br />'+ */
            desc_user +
            '</div>');
            $('.modal-footer').html(
                '<a class="btn btn-primary" href="/Iniciativa/' + IdMember + '">Ver Iniciativas</a>' +
                '<button type="button" class="btn btn-default" data-dismiss="modal">Fechar</button>');
            $('#myModal').modal('show');
        },
        error: function () {
            alert("Erro ao devolver valor")
        }
    });
}

//prienche tabela com dados de tramite
function showTramite(XmlData, link, tbody) {
    tbody.empty();
    var tituloDoc = $(XmlData).find('item doctitle');
    var dataDoc = $(XmlData).find('item docstatus_date');
    var idDoc = $(XmlData).find('item docdoc_id');
    var subtitleDoc = $(XmlData).find('item docsub_title');
    for (var i = 0; i < $(XmlData).find('item').length; i++) {
        var dataDocObj = $(dataDoc[i]).text().split('T');
        tbody.append('<tr><td class="small"><i class="fa fa-folder-o" aria-hidden="true"></i> &nbsp; ' +
        '<a href="/' + link + '/' + $(idDoc[i]).text() + '">' + $(tituloDoc[i]).text() + '</a>' +
        '</td><td class="small">' + $(subtitleDoc[i]).text()+ '</td>' +
        '<td class="small" id="datadocumento">' + dataDocObj[0] + '</td></tr>');
    }
}

//ajax que chama diplomas de acordo com tiopo de Lei
function callDiplome(docType, pageNumber, elementsPerPage, tbody, tPager) {
    content = $('#leiscontainer');
    link = "/ListaT/" + (((pageNumber - 1) * elementsPerPage) + 1) + "/" + (elementsPerPage -1) + "/" + docType;
    $.ajax({
        url: link,
        success: function (data) {
            $.ajax(
                {
                    url: "http://localhost:8089/documentstypecount/" + docType,
                    success: function (data) {
                        var pages = Math.ceil(JSON.parse(data)[0].numberofmembers_ / elementsPerPage);
                        if (pages > 1) {
                            tPager.removeClass("hide");
                            tPager.bootpag({ total: pages });
                        }
                        else {
                            tPager.addClass("hide");
                        }
                    },
                }
            );
            showTramite(data, 'docLei', tbody);
        },
        error: function (data) {
            alert("erro ao devolver valor")
        }
    });
}

//prienche tabela de tramites
function priencheTable(data, tDoc, workflow) {
    var DocProgramado = data;
    var tam = $(DocProgramado).find('sittingend_date').length;
    var local = $(DocProgramado).find('venueshort_name');
    var dataInicio = $(DocProgramado).find('sittingstart_date');
    var tipoDoc = $(DocProgramado).find(tDoc);
    x = parseInt($(DocProgramado).find('TotalDoc').text());

    $('#tableT').dataTable().fnClearTable();
    for (i = 0; i < tam; i++) {
        //insere dados na tabela
        dataT = dataInicio[i].textContent.split('T');
        dataC = [workflow[tipoDoc[i].textContent], local[i].textContent, alterFormatData(dataT[0])];
        $('#tableT').dataTable().fnAddData(dataC);
    }
}

//verifica tipo de Tramites e atribui link
function verifyTypeTramite(start_date, end_date, documento, LimiteInf) {
    //ajax que faz pesquisa de tramite
    link = "/TramiteDocumento/" + Limitepag + "/4/0-00-0000/0-00-0000/";
    tDoc = 'sittingmeeting_type';

    if (start_date != '') {
        datas = '/' + start_date + '/' + end_date;
    } else {
        datas = '/0-00-0000/0-00-0000';
    }
    if (documento.trim() == "Sessões") {
        $('#titleh').text('Sessões');
        link = '/TramiteDoc/' + LimiteInf + datas;
        tDoc = 'sittingmeeting_type';
    } else {
        $('#titleh').text('Tipo Documento');
        link = "/TramiteDocumento/" + LimiteInf + datas;
        tDoc = 'itemschedule_item_type'
    }
}

function configuraPaginacao(numpag) {
    $('.memberPagination').bootpag({
        total: numpag,
        page: 1,
        maxVisible: 4,
        leaps: true,
        firstLastUse: true,
        first: '←',
        last: '→',
        wrapClass: 'pagination',
        activeClass: 'active',
        disabledClass: 'disabled',
        nextClass: 'next',
        prevClass: 'prev',
        lastClass: 'last',
        firstClass: 'first'
    });
}

//ajax responsável por fazer chamada em paginação
function ClickPagination(caminho, contexto) {
    var div_html = $('.commentlist');
    $.ajax({
        url: caminho,
        success: function (data) {
            div_html.empty();
            var xml_data = data;
            /*Faz Listagem de membros*/
            showmembres(xml_data, contexto);
        },
        error: function (data) {
            alert("erro ao devolver valor")
        }
    });
}

// retorna total de elementos por página
function getTotalCount(link, link1) {
    //obtem total de registo por paginação
    $.ajax({
        url: link1,
        success: function (dat) {
            x = parseInt(dat);
            configuraPaginacao(x);
            ClickPagination(link);
        },
        error: function (dat) {
            alert("erro ao devolver valor")
        }
    });
}

//função responsável por fazer pesquisa de Deputados (recebe, nome e o partido)
function getShearchMember(div, nome, partido) {
    content = $(div);
    if (partido.length == 0) {
        partido = '0';
    }
    if (nome.length == 0) {
        nome = '0';
    }

    link = '/DeputadosProcura/1/5/' + nome + '/' + partido;

    if (nome != 0 || partido != 0) {
        $.ajax({
            url: link,
            success: function (data) {
                content.empty();
                showmembres(data);

                //obtem total de registo por paginação
                getTotalCount(link, '/CountMember/' + nome + '/' + partido);
            },
            error: function () {
                alert("erro ao devolver valor");
            }
        });
    }
    if (nome == 0 && partido == 0) {
        link = "/DeputadoList/" + 1 + "/" + 4
        $.ajax({
            url: link,
            success: function (data) {
                content.empty();

                var xml_data = data;
                /*Faz Listagem de membros*/
                showmembres(xml_data);
                getTotalCount(link, '/DeputadoTotal/' + 1);
            },
            error: function () {
                alert("erro ao devolver valor")
            }
        });
    }
}

$(function () {

    //altera formulário de pesquisa avançado de acordo com a escolha veita no select
    $('.tipoPesquisa').change(function () {
        item = $(this).val();
        vhtml = $('.checkbox');
        check1 = "'p_membros'", check2 = "'p_doc'", check3 = "'p_nome'";

        htmlbase = '<div class="col-md-12 nopadding">' +
                    '<form onsubmit="return false;">' +
                    '<div class="row checkbox nopadding nomargingLeft">' +
                        '<div class="col-md-12 nopadding">' +
                            '<div class="col-md-3 nopadding">' +
                                '<label><input class="p_membros" type="checkbox" value="1">Membros</label>' +
                            '</div>' +
                            '<div class="col-md-3 nopadding">' +
                                '<label><input class="p_doc" type="checkbox" value="2">Documentos</label>' +
                            '</div>' +
                            '<div class="col-md-3 nopadding">' +
                                '<label><input class="p_nome" type="checkbox" value="3" >Nome Comissão</label>' +
                            '</div>' +
                            '<div class="col-md-3 nopadding">' +
                                '<label><form><input type="checkbox" onclick="desabeCheck(this.id,' + check1 + ',' + check2 + ',' + check3 + ')" class="p_documento" id="p_documento" value="All" >Todos</label>' +
                            '</div>' +
                            '<div class="col-md-3 nopadding">' +
                                '<button class="ver" onclick="verPesquisa()">Mostrar</button></form>' +
                            '</div>' +
                        '</div>' +
                    '</div>' +
                    '</form>' +
                '</div>';

        if (item == 'documento') {
            vhtml.empty();
            check1 = "'p_titulo'", check2 = "'p_texto'", check3 = "'p_intervenientes'";

            htmDocumento = '<div class="col-md-12 nopadding">' +
                            '<div class="row checkbox nopadding nomargingLeft">' +
                                '<div class="col-md-12 nopadding">' +
                                    '<div class="col-md-3 nopadding">' +
                                        '<label><input class="p_titulo" type="checkbox" value="1">Título</label>' +
                                    '</div>' +
                                    '<div class="col-md-3 nopadding">' +
                                        '<label><input class="p_texto" type="checkbox" value="2">Todo o texto</label>' +
                                    '</div>' +
                                    '<div class="col-md-3 nopadding">' +
                                        '<label><input class="p_intervenientes" type="checkbox" value="3" >Intervenientes</label>' +
                                    '</div>' +
                                    '<div class="col-md-3 nopadding">' +
                                        '<label><form><input type="checkbox" onclick="desabeCheck(this.id,' + check1 + ',' + check2 + ',' + check3 + ')" class="p_documento" id="p_documento" value="All" >Todos</label>' +
                                    '</div>' +
                                    '<div class="col-md-3 nopadding">' +
                                        '<button class="ver" onclick="verPesquisa()">Mostrar</button></form>' +
                                    '</div>' +
                                '</div>' +
                            '</div>' +
                        '</div>';

            vhtml.html(htmDocumento);
        } else {
            vhtml.empty();
            vhtml.html(htmlbase);
        }
    });

    //faz chamada do serviço para listar o resultado da pesquisa

    $('.titulo').keypress(function (e) {
        if (e.which == 13) {
            verPesquisa();
        }
    });
});

function verPesquisa() {
    var selected = [];
    $('.checkbox input:checked').each(function () {
        selected.push($(this).attr('value'));
    });
    valor = $('.titulo').val();
    tipoPesquisa = $('.tipoPesquisa').val();
    param = CreateUrl(tipoPesquisa, selected, valor);
    endpoint = '';

    if (tipoPesquisa == 'documento') {
        endpoint = 'getdocsearch';
    }
    if (tipoPesquisa == 'comissao') {
        endpoint = 'getcommitteesearch';
    }
    if (tipoPesquisa == 'grupo') {
        endpoint = 'getpoliticalgroupsearch';
    }

    ULR = 'ResultadoPesquisa_Avancada/' + endpoint + param;

    conteudo = $('#result');
    //faz chamada ao serviço "getResultadoPesquisaAvancada"
    if (valor.length > 2) {
        $.ajax({
            url: ULR,
            success: function (data) {
                conteudo.empty();
                showSearch(data, conteudo, tipoPesquisa);//apresenta dados de pesquisa
            },
            error: function () {
                alert("erro ao devolver valor")
            }
        });
    }
}

function showSearch(xml, conteudo, tipoPesquisa) {
    tam = $(xml).find('item').length;
    msn = '';
    doctitle = 'doctitle';

    if (tam == 0) {
        msn = '<span class="semRegisto">Sem registo</span>';
        conteudo.append(msn);
    }
    if (tipoPesquisa == 'comissao') {
        doctitle = 'group_full_name';
    }

    tituloAnterior = '';
    for (i = 0; i < tam; i++) {
        titulo = $($($(xml).find('item')[i]).find(doctitle)).text();
        estado = $($($(xml).find('item')[i]).find('docstatus')).text();
        body = $($($(xml).find('item')[i]).find('docbody')).text();
        /*doc_id = $($($(xml).find('item')[i]).find('docdoc_id')).text();*/

        Lasttitulo = $($($(xml).find('item')[i + 1]).find(doctitle)).text();;

        if (titulo != Lasttitulo) {
            conteudo.append('<tr>' +
            '<td width="100%">' +
            '<a href="#">' + titulo + '</a>' +
            '<span class="estadoDoc">&nbsp;&nbsp;&nbsp;&nbsp;Estado: ' + estado + '</span>' +
            '</td>' +
            '</tr><td></td>');
        }

    }
}

//verifica campos de pesquisa e retorna link
function CreateUrl(tipo, fields, valor) {
    url = '';
    cutUrl1 = 0, cutUrl2 = 0, cutUrl3 = 0;

    if (valor.length != 0) {
        if (tipo != '') {
            if (fields[0] == 'All') {
                url = url + '/' + valor + '/' + valor + '/' + valor;
            } else {
                for (i = 0; i < fields.length; i++) {
                    if (fields[i] == 1) {
                        cutUrl1 = valor;
                    }
                    if (fields[i] == 2) {
                        cutUrl2 = valor;
                    }
                    if (fields[i] == 3) {
                        cutUrl3 = valor;
                    }
                }
                url = url + '/' + cutUrl1 + '/' + cutUrl2 + '/' + cutUrl3;
            }
        } else {
        }

        return url;
    }
}

//ativa ou desativa os campos de pesquisa
function enableORdisable(status, check1, check2, check3) {
    $('.' + check1).attr('disabled', status);
    $('.' + check2).attr('disabled', status);
    $('.' + check3).attr('disabled', status);
    //unckeched if exists
    $('.' + check1).attr('checked', false);
    $('.' + check2).attr('checked', false);
    $('.' + check3).attr('checked', false);
}

function desabeCheck(id, check1, check2, check3) {
    v_documento = id;
    var checked = $("#" + id + ":checked").length;

    if (checked != 0) {
        enableORdisable(true, check1, check2, check3);
    } else {
        enableORdisable(false, check1, check2, check3);
    }
}

function geraprintPdf(documenthistory) {
    print = $('.print');
    var href = print.attr('href');
    print.attr('href', href + '/' + $(documenthistory).find('docaudit_id')[0].textContent);
    print.attr('title', 'Imprimir em pdf');
}

$(function () {
    $('.tab-2').show();
});

