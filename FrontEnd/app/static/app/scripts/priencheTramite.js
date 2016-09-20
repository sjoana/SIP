/**
 * Created by emanuel on 7/28/15.
 */
function priencheTramite(documenthistory, workflow, idDoc){

    $(function() {
        var tableHistory = $('.tableH').dataTable({
            "bFilter": false,
            "bLengthChange": false,
            "info": false,
            "bRetrieve": true,
            "ordering": false
        });

        var tableVersion = $('.tableV').dataTable({
            "bFilter": false,
            "bLengthChange": false,
            "info": false,
            "bRetrieve": true,
            "ordering": false
        });

        $( "#tabs" ).tabs();

        var tam            = $(documenthistory).find('item').length;
        var docBody        = $('article');
        var docMembers     = $('.commentlist');
        var docDocument    = $('#tabs-3');

        docBody.empty();
        docMembers.empty();
        docDocument.empty();

        doctext = $(documenthistory).find('item docbody');
        docData = $(documenthistory).find('item docstatus_date');
        docStatus = $(documenthistory).find('item docstatus');

        docBody.append($(doctext[0]).text());
        docDocument.append('Não existem documentos associados');

        var tm = $(workflow).find('state').length;
        $('#leiHistory').empty();

        for (i=0; i<tam; i++ ){

            Desc = '<i class="fa fa-check-square-o"></i> ' + workflow[$(docStatus[i]).text()];
            dataDocObj = $(docData[i]).text().split('T');

            //inseri dados na tabela versão
            data= ['Versão'+(i+1),dataDocObj[0]];
            tableVersion.fnAddData(data);

            //inseri dados na tabela historico Lei
            data= [Desc,dataDocObj[0]];
            tableHistory.fnAddData(data);
        }

        $('article').readmore({
            speed: 500,
            collapsedHeight: 565
        });
    });

    $('#IconDoc').click(function(){
        $.ajax({
            url: '/DocumentoAssociado/'+idDoc+'/0',
            success: function (xml) {
                xmlData = xml;
                apresentaDados(xmlData);//apresenta dados
            },
            error: function () {
                alert(this.url);
            }
        });
    });
}

function apresentaDados(XmlData) {
    
    var x = $($(xmlData)[1]);
    if (x.children().length == 0) $('.tab3').html('<p>Não existem documentos associados</p>');
    else
    {
        var cnt = x.children().length;
        //var lli = document.createElement("ul");
        $('.tab3').empty();
        //$('.tab3').append(lli);
        //alert(x);.length
        for (var i = 0; i < cnt; i++)
        {
            var item = x.children()[i];
            doctitle = item.children[35].childNodes[0].data;
            dochead_id = item.children[32].childNodes[0].data;
            $('.tab3').append('<div><i class="fa fa-file-o" aria-hidden="true"></i> &nbsp; <a href="/DocumentoAssociado/' + dochead_id + '/' + (i + 1) + '">' + doctitle + '</a></div>');
        }
       
    }
    
    //$.each( x.children, function(i, item) {
    //    alert(item.docstatus_date);
    //});​

    //$($(xmlData).root)

    //doctitle = $(xmlData).find('item doctitle').text();
    //dochead_id = $(xmlData).find('item dochead_id').text();

    //if (doctitle.length == 0) $('.tab3').html('<span>Não existem documentos associados</span>');
    //else $('.tab3').html('<span><a href="/DocumentoAssociado/'+dochead_id+'/1">'+doctitle+'</a></span>');
}


