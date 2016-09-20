function populateAgenda(sittingsDocument){

    var agendamentos = $(sittingsDocument).find('item');
    var temp = '[';
    var typeDoc;
    var url='';

    for (var i=0;i<agendamentos.length;i++) {
        typeDoc = $(agendamentos[i]).find('itemschedule_item_type').text();
        if (typeDoc == 'projeto_lei'){
            url = '/docLeiModal/';
        }
        if(typeDoc == 'assembly_question'){
            url = '/docPerguntaModal/';
        }

        id = $(agendamentos[i]).find('itemschedule_item_id').text();
        temp +='{"id":"'+i+'",';
        temp +='"title":"'+$(agendamentos[i]).find('doctitle').text()+' - ('+$(agendamentos[i]).find('venueshort_name').text()+')<br>",';
        temp +='"url":"'+url+id+'",';
        if($(agendamentos[i]).find('sittingmeeting_type').text()=='plenary')
        temp +='"class":"event-success",';
        else
            temp +='"class":"event-info",';
        temp +='"start":"'+$(agendamentos[i]).find('sittingstart_date').text()+'",';
        temp +='"end":"'+$(agendamentos[i]).find('sittingend_date').text()+'"}';
        if((i+1)<agendamentos.length)
            temp +=',';
    }
    temp += ']';

    return JSON.parse(temp);;
}
