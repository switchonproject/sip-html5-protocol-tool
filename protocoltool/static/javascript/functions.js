
function writeLabelLine(tablebody, label, text){
    /*
    write a line of text with a label to a table.
    */

    $(tablebody).append(
          '<tr><td class="col-md-2 infotext"><strong>' + label + '</strong></td>' +
          '<td class="col-md-10 infotext">' + text + '</td></tr>')
}

function writeLinksLine(tablebody, label, text, w1='2', w2='10'){
    /*
    write a line of links with a label to a table.
    */

    text = text.split(" ");
    var urlRegex = /[-a-zA-Z0-9@:%_\+.~#?&//=]{2,256}\.[a-z]{2,4}\b(\/[-a-zA-Z0-9@:%_\+.~#?&//=]*)?/gi;
    var total_str=''

    for ( var i =0; i < text.length; i++ ){
        var word=text[i]

        // Is a url
        if (word.match(urlRegex)) {
            var url = word.replace(/^\s+|\s+$/g, '');
            if (word.includes("http"))    total_str += '<a href=' + url + ' target="_blank">' + url + '</a><br>';
            else                          total_str += '<a href=http://' + url + ' target="_blank">' + url + '</a><br>';
        }
        // Is just text
        else {
            total_str += (word + " ");
        }
    }
    $(tablebody).append(
      '<tr><td class="col-md-'+w1+' infotext"><strong>' + label + '</strong></td>' +
      '<td class="col-md-'+w2+' infotext">' + total_str + '</td></tr>')

}

function writeLabelTwoLines(tablebody, label, text){
    /*
    write a line of text with a title for the experiment info in the form
    */
    $(tablebody).append(
          '<tr><td class="infotext"><strong>' + label + '</strong><br>' + text + '</td></tr>')
}

function removePartnerErrorClasses() {

    $('#id_partner_name').removeClass('error');
    $('#id_partner_email').removeClass('error');
    $('#id_partner_organisation').removeClass('error');
}

function removePublicationErrorClasses() {
    $('#id_publication_name').removeClass('error');
    $('#id_publication_type').removeClass('error');
}

function writePublicationsViewProtocol(publications, table) {
    var nrPublications = publications.length;
    for(i = 0; i < nrPublications; i++){
        writeLinksLine("#" + table + " > tbody", publications[i].name, publications[i].type, w1='10', w2='2');
    }
}

function writeStepsViewProtocol(steps, table) {

    var nrSteps = steps.length;

    for(i = 0; i < nrSteps; i++){

        doneText = "Task " + steps[i].taskNr

        if(steps[i].done == 'True'){
            doneText += " (Done):";
        }
        else {
            doneText += " (In progress):";
        }

        writeLabelLine("#" + table + " > tbody", doneText, steps[i].task);
        writeLinksLine("#" + table + " > tbody", "Description:", steps[i].properties);
        if (steps[i].links !== "") {
            writeLinksLine("#" + table + " > tbody", "Links:", steps[i].links);
        }
        writeLabelLine("#" + table + " > tbody", "Task leader:", steps[i].partnerName);
        writeLabelLine("#" + table + " > tbody", "Deadline:", steps[i].deadline);
        writeLabelLine("#" + table + " > tbody", "", "");
    }
}


function writePartnersViewProtocol(partners) {
    /*
    TODO: Implement this function. It somehow does not work yet as all partners are duplicated.
    */
    var nrPartners = partners.length;

    for(i = 0; i < nrPartners; i++){

        var leadText = ""
        if(partners[i].lead == 'True'){
            leadText = "lead"
        }

        $('#partnerTableView > tbody').append(
            '<tr><td class="col-md-3 infotext">' + partners[i].name + '</td>' +
            '<td class="col-md-3 infotext">' + partners[i].email + '</td>' +
            '<td class="col-md-3 infotext">' + partners[i].organisation + '</td>' +
            '<td class="col-md-1 infotext"><strong>' + leadText + '</strong></td></tr>'
        )
    }
}


function removeReqErrorClasses() {

    $('#id_req_task').removeClass('error');
    $('#id_req_properties').removeClass('error');
    $('#partnerDataReq').removeClass('error');
    $('#id_req_deadline').removeClass('error');
}

function removeExpErrorClasses() {

    $('#id_exp_task').removeClass('error');
    $('#id_exp_properties').removeClass('error');
    $('#partnerExpStep').removeClass('error');
    $('#id_exp_deadline').removeClass('error');
}

function removeReportingErrorClasses() {

    $('#id_reporting_task').removeClass('error');
    $('#id_reporting_properties').removeClass('error');
    $('#partnerReporting').removeClass('error');
    $('#id_reporting_deadline').removeClass('error');
}

function checkValidField(item){
    /*
    check if a field in the form has any contents (is filled in)
    */
   var valuestr = item.val();
   var ishtml = /<[a-z][\s\S]*>/i.test(valuestr);
   if (valuestr === null || valuestr === "" || ishtml) {
        item.addClass('error');
        return false;
    }
    else {
        item.removeClass('error');
        return true;
    }
}

function checkValidEmail(item){
    /*
    check if a field in the form has any contents (is filled in)
    */
   if(item.val() === null || item.val() === "" ){
        item.addClass('error');
        return false;
    }
    else {
        item.removeClass('error');
        return true;
    }
}


function validateEmail(item)
{
    var inputText = item.val();
    var mailformat = /^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$/;

    if(inputText.match(mailformat))
    {
        item.removeClass('error');
        return true;
    }
    else
    {
        item.addClass('error');
        return false;
    }
}


function checkValidDate(item) {
    // input is always (standard for date field HTML5) YYYY-mm-dd
    dateString = item.val();
    var bits = dateString.split('-');
    var d = new Date(bits[0], bits[1] - 1, bits[2]);

    if(d && (d.getMonth() + 1) == bits[1]){
        item.removeClass('error');
        return true;
    }
    else{
        item.addClass('error');
        return false;
    }
}

function warningPopup(messageText){
    /*
    Show a warning message using the bootbox library
    */
     bootbox.alert(messageText, function() {
         console.log("Alert Callback");
     });
}

function finish() {
    /*
    user presses the finish button; check if full name and short name are filled in
    */
    // check if all values are valid
    validShortname = checkValidField($('#id_basic_shortTitle'));
    validTitle = checkValidField($('#id_basic_title'));
    validIdea = checkValidField($('#id_basic_experimentIdea'));
    validHypothesis = checkValidField($('#id_basic_hypothesis'));
    validObjective = checkValidField($('#id_basic_researchObjective'));

    if (validShortname === true && validTitle === true && validIdea === true && validHypothesis === true && validObjective === true){
//        bootbox.confirm('Experiment information that is not saved will be lost. Are you sure you wish to close the form?', function(result){
//            if(result){
//                $('#dataset_form').submit();
//            }
//        });
        $('#dataset_form').submit();
    }
    else {
        bootbox.confirm('No valid full experiment name or short name. Are you sure you wish to go back to the participate tool?', function(result){
            if(result){
                $('#dataset_form').submit();
            }
        });
    }
}


function setMessage(messagetype, messagefa, messagetext){
    /*
    Set the message text to the box on top of the page
    messagetype: from bootstrap; can be "alert alert-success",
    messagefa: the class info of the font awesome icon to use
    messagetext: string containing the text
    */
	try {
		$('#messagetype').removeClass().addClass(messagetype);
		$('#messagefa').removeClass().addClass(messagefa);
		$('#messagetext').text(messagetext);
	}
		catch(err) {
			console.log(err.message);
	}
}


function refreshAll(){
    /*
    Refresh all form sections
    */
    refreshExperimentInfo();
    refreshPartners();
    refreshPublications();
    refreshReqs(existingReqs);
    refreshExpSteps(existingExpSteps);
    refreshReporting(existingReportings);
}


function refreshExperimentInfo(){

    $("#experimentTable tbody tr").remove();

    writeLabelTwoLines("#experimentTable > tbody", "Full name:", existingExperimentInfo.title);
    writeLabelTwoLines("#experimentTable > tbody", "Short name:", existingExperimentInfo.shortTitle);
    writeLabelTwoLines("#experimentTable > tbody", "Idea:", existingExperimentInfo.experimentIdea);
    writeLabelTwoLines("#experimentTable > tbody", "Hypothesis:", existingExperimentInfo.hypothesis);
    writeLabelTwoLines("#experimentTable > tbody", "Objective:", existingExperimentInfo.researchObjective);
}

function refreshPartners() {
    // Reset all Partner stuff
    $('#id_partner_name').val("");
    $('#id_partner_email').val("");
    $('#id_partner_organisation').val("");
    $('#id_partner_lead').prop('checked', false);

    // update buttons
    $('#updatePartnerID').removeClass( "active" ).addClass( "disabled" );
    $('#updatePartnerID').prop( "disabled", true);
    $('#deletePartnerID').removeClass( "active" ).addClass( "disabled" );
    $('#deletePartnerID').prop( "disabled", true);

    // reset selected partner ID
    $('#selectedPartnerID').val('-99')

    // reset partner table
    var arrayLength = existingPartners.length;
    $("#partnerTable tbody tr").remove();

    for (i = 0; i < arrayLength; i++) {
        var leadText = "";
        if (existingPartners[i].lead == 'True'){
            leadText = "<strong>lead</strong>"
        }

        $("#partnerTable > tbody").append('<tr class="partnerRow"><td class="col-md-5 partnername">' + existingPartners[i].name +
        '<td class="col-md-5">' + existingPartners[i].organisation + '</td><td class="col-md-2">' + leadText + '</td></tr>');
    }

    // refresh partners in the reqs table
    selectedPartnerID = $("#partnerDataReq").val()  // temporary store selected partner
    $("#partnerDataReq").empty();
    for (i = 0; i < arrayLength; i++) {
        $("#partnerDataReq").append('<option value = ' + existingPartners[i].id + '>' + existingPartners[i].name + '</option>');
    }
    $("#partnerDataReq").val(selectedPartnerID)

    // refresh the partners in exp steps table
    selectedPartnerID = $("#partnerExpStep").val()  // temporary store selected partner
    $("#partnerExpStep").empty();
    for (i = 0; i < arrayLength; i++) {
        $("#partnerExpStep").append('<option value = ' + existingPartners[i].id + '>' + existingPartners[i].name + '</option>');
    }
    $("#partnerExpStep").val(selectedPartnerID)

    // refresh partners in reporting table
    selectedPartnerID = $("#partnerReporting").val()  // temporary store selected partner
    $("#partnerReporting").empty();
    for (i = 0; i < arrayLength; i++) {
        $("#partnerReporting").append('<option value = ' + existingPartners[i].id + '>' + existingPartners[i].name + '</option>');
    }
    $("#partnerReporting").val(selectedPartnerID)
}

function refreshPublications(){
    // Reset all Publication stuff
    $('#id_publication_name').val("");
    $('#id_publication_type').val("");

    // update buttons
    $('#updatePublicationID').removeClass( "active" ).addClass( "disabled" );
    $('#updatePublicationID').prop( "disabled", true);
    $('#deletePublicationID').removeClass( "active" ).addClass( "disabled" );
    $('#deletePublicationID').prop( "disabled", true);

    // reset selected publication ID
    $('#selectedPublicationID').val('-99')

    // reset publication table
    var arrayLength = existingPublications.length;
    $("#publicationTable tbody tr").remove();

    for (i = 0; i < arrayLength; i++) {
        $("#publicationTable > tbody").append('<tr class="publicationRow"><td class="col-md-8 publicationname">' + existingPublications[i].name + '</td>' + '</tr>');
    }
}


function refreshReqs(existingList){

    existingReqs = existingList;

    // CLEAR TABLE AND FORM
    $('#id_req_done').prop('checked', false)
    $('#id_req_task').val("")
    $('#id_req_properties').val("")
    $('#id_req_links').val("")

    $("#partnerDataReq").empty();
    var arrayLength = existingPartners.length;
    for (i = 0; i < arrayLength; i++) {
        $("#partnerDataReq").append('<option value = ' + existingPartners[i].id + '>' + existingPartners[i].name + '</option>');
    }
    $("#partnerDataReq").val(null)

    setButtonsReq(false);    // update buttons

    // rebuild table overview
    var arrayLength = existingReqs.length;
    $("#reqTableID tbody tr").remove();

    if(arrayLength == 0){
        $("#reqTableID > tbody").append(
            '<tr><td class="col-md-8">...</td>' +
            '<td class="col-md-4"></td></tr>')
    }

    for (i = 0; i < arrayLength; i++) {

        var taskDone = 'No'
        if (existingReqs[i].done == 'True'){
            taskDone = 'Yes'
        }

        $("#reqTableID > tbody").append(
            '<tr id = ' +  existingReqs[i].id + '>' +
            '<td class="col-md-1">' + existingReqs[i].taskNr + '</td>' +
            '<td class="col-md-7">' + existingReqs[i].task + '</td>' +
            '<td class="col-md-2">' + existingReqs[i].deadline + '</td>' +
            '<td class="col-md-2">' + taskDone + '</td></tr>')
    }


    // SET TABLE AND FORM TO SELECTED REQUIREMENT
    selectedID = $('#selectedReqID').val();
    parent = $('#reqTableID');
    $('#' + selectedID, parent).addClass("highlight").siblings().removeClass("highlight"); // highlight selected row

    var nrSteps = existingReqs.length;

    for (i = 0; i < nrSteps; i++) {

        if (existingReqs[i].id == selectedID){

            removeReqErrorClasses();                // remove all error classes

            $('#id_req_task').val(existingReqs[i].task);
            $('#id_req_properties').val(existingReqs[i].properties);
            $('#id_req_links').val(existingReqs[i].links);
            $('#id_req_deadline').val(existingReqs[i].deadline);

            if(existingReqs[i].done == 'True'){
                $('#id_done').prop('checked', true);
            }
            else{
                $('#id_done').prop('checked', false);
            }

            contrPartner = getPartnerByID(existingReqs[i].partnerID);

            $('#partnerDataReq').val(contrPartner.id);
            setButtonsReq(true); // update buttons
        }
    } // end for
} // end refreshReqs


function refreshExpSteps(existingList){

    // use the existingexpsteps by default; however, if a new list is given to the refresh function
    // by updating, deleting, etc. in this way the new list can be passed to the refresh function
    existingExpSteps = existingList

    // CLEAR TABLE AND FORM
    $('#id_exp_task').val("")
    $('#id_exp_properties').val("")
    $('#id_exp_links').val("")

    $("#partnerExpStep").empty();
    var arrayLength = existingPartners.length;
    for (i = 0; i < arrayLength; i++) {
        $("#partnerExpStep").append('<option value = ' + existingPartners[i].id + '>' + existingPartners[i].name + '</option>');
    }
    $("#partnerExpStep").val(null)

    setButtonsExpStep(false);    // update buttons


    var arrayLength = existingExpSteps.length;
    $("#expStepTableID tbody tr").remove();

    if(arrayLength == 0){
        $("#expStepTableID > tbody").append(
            '<tr><td class="col-md-8">...</td>' +
            '<td class="col-md-4"></td></tr>')
    }

    for (i = 0; i < arrayLength; i++) {

        var taskDone = 'No'
        if (existingExpSteps[i].done == 'True'){
            taskDone = 'Yes'
        }

        $("#expStepTableID > tbody").append(
            '<tr id = ' +  existingExpSteps[i].id + '>' +
            '<td class="col-md-1">' + existingExpSteps[i].taskNr + '</td>' +
            '<td class="col-md-7">' + existingExpSteps[i].task + '</td>' +
            '<td class="col-md-2">' + existingExpSteps[i].deadline + '</td>' +
            '<td class="col-md-2">' + taskDone + '</td></tr>')
    }


    // SET TABLE AND FORM TO SELECTED EXP STEP
    selectedID = $('#selectedExpStepID').val();
    parent = $('#expStepTableID');
    $('#' + selectedID, parent).addClass("highlight").siblings().removeClass("highlight"); // highlight selected row

    var nrSteps = existingExpSteps.length;

    for (i = 0; i < nrSteps; i++) {

        if (existingExpSteps[i].id == selectedID){

            removeExpErrorClasses();                // remove all error classes

            $('#id_exp_task').val(existingExpSteps[i].task);
            $('#id_exp_properties').val(existingExpSteps[i].properties);
            $('#id_exp_links').val(existingExpSteps[i].links);
            $('#id_exp_deadline').val(existingExpSteps[i].deadline);

            if(existingExpSteps[i].done == 'True'){
                $('#id_done').prop('checked', true);
            }
            else{
                $('#id_done').prop('checked', false);
            }

            contrPartner = getPartnerByID(existingExpSteps[i].partnerID);
            $('#partnerExpStep').val(contrPartner.id);
            setButtonsExpStep(true); // update buttons
        }
    } // end for

}

function refreshReporting(existingList){

    // use the existingreportings by default; however, if a new list is given to the refresh function
    // by updating, deleting, etc. in this way the new list can be passed to the refresh function
    existingReportings = existingList

    $('#id_reporting_task').val("")
    $('#id_reporting_properties').val("")
    $('#id_reporting_links').val("")

    $("#partnerReporting").empty();
    var arrayLength = existingPartners.length;
    for (i = 0; i < arrayLength; i++) {
        $("#partnerReporting").append('<option value = ' + existingPartners[i].id + '>' + existingPartners[i].name + '</option>');
    }
    $("#partnerReporting").val(null)

    setButtonsReporting(false); // update buttons

    var arrayLength = existingReportings.length;
    $("#reportingTableID tbody tr").remove();

    if(arrayLength == 0){
        $("#reportingTableID > tbody").append(
            '<tr><td class="col-md-8">...</td>' +
            '<td class="col-md-4"></td></tr>')
    }

    for (i = 0; i < arrayLength; i++) {

        var taskDone = 'No'
        if (existingReportings[i].done == 'True'){
            taskDone = 'Yes'
        }

        $("#reportingTableID > tbody").append(
            '<tr id = ' +  existingReportings[i].id + '>' +
            '<td class="col-md-1">' + existingReportings[i].taskNr + '</td>' +
            '<td class="col-md-7">' + existingReportings[i].task + '</td>' +
            '<td class="col-md-2">' + existingReportings[i].deadline + '</td>' +
            '<td class="col-md-2">' + taskDone + '</td></tr>')
    }


    // SET TABLE AND FORM TO SELECTED EXP STEP
    selectedID = $('#selectedReportingID').val();
    parent = $('#reportingTableID');
    $('#' + selectedID, parent).addClass("highlight").siblings().removeClass("highlight"); // highlight selected row

    var nrSteps = existingReportings.length;

    for (i = 0; i < nrSteps; i++) {

        if (existingReportings[i].id == selectedID){

            removeReportingErrorClasses();                // remove all error classes

            $('#id_reporting_task').val(existingReportings[i].task);
            $('#id_reporting_properties').val(existingReportings[i].properties);
            $('#id_reporting_links').val(existingReportings[i].links);
            $('#id_reporting_deadline').val(existingReportings[i].deadline);

            if(existingReportings[i].done == 'True'){
                $('#id_done').prop('checked', true);
            }
            else{
                $('#id_done').prop('checked', false);
            }

            contrPartner = getPartnerByID(existingReportings[i].partnerID);
            $('#partnerReporting').val(contrPartner.id);
            setButtonsReporting(true); // update buttons
        }
    } // end for
} // end refreshReporting

function getPartnerByID(partnerID){
    /*
    Search for a partner by their ID
    */
    var nrPartners = existingPartners.length;

    for (j = 0; j < nrPartners; j++) {
        if(existingPartners[j].id == partnerID){
            return existingPartners[j];
        }
    }

    return null;
}


function sendPublicationInfoToServer(update){

    url = "/project/addpublication/"

    dataToSend = {
       datasetID: datasetID,
       name: $('#id_publication_name').val(),
       type: $('#id_publication_type').val(),
       csrfmiddlewaretoken: csrfmiddlewaretoken
    }

    if (update == true){
        url = "/project/updatepublication/"
        publicationID = $('#selectedPublicationID').val();
        dataToSend['publicationID'] = publicationID;
    }

    $('#selectedPublicationID').val(-1) // deselect the publication after storing the form data

    $.ajax({
        url: url,
        type: "POST",
        data: dataToSend,

        // handle a successful response
        success : function(json) {
            existingPublications = JSON.parse(json['existingPublicationsJSON']);
            refreshPublications();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

} // end sendPublicationInfoToServer


function sendPartnerInfoToServer(update){

    url = "/project/addpartner/"

    var lead = 'False';
    if($('#id_partner_lead').is(':checked')){

        var existingLead = false;
        selectedPartnerID = $('#selectedPartnerID').val() // for update, store current selected partner

        // check if there is already a lead partner
        var nrPartners = existingPartners.length;
        for (j = 0; j < nrPartners; j++) {

            if(update === true){
                if(existingPartners[j].lead == 'True' && existingPartners[j].id != selectedPartnerID){
                    existingLead = true;
                }
            }
            if(update === false){
                if(existingPartners[j].lead == 'True'){
                    existingLead = true;
                }
            }
        }

        if(existingLead == true){
            warningPopup('There is already a partner in the lead; ' +
                         'please uncheck the lead box or change the existing partner in the lead')
            return;
        }
        else{
           lead = 'True';
        }
    }

    dataToSend = {
       datasetID: datasetID,
       name: $('#id_partner_name').val(),
       email: $('#id_partner_email').val(),
       organisation: $('#id_partner_organisation').val(),
       lead: lead,
       csrfmiddlewaretoken: csrfmiddlewaretoken
    }

    if (update == true){
        url = "/project/updatepartner/"
        partnerID = $('#selectedPartnerID').val();
        dataToSend['partnerID'] = partnerID;
    }

    $('#selectedPartnerID').val(-1) // deselect the partners after storing the form data

    $.ajax({
        url: url,
        type: "POST",
        data: dataToSend,

        // handle a successful response
        success : function(json) {
            existingPartners = JSON.parse(json['existingPartnersJSON']);
            refreshPartners();
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });

} // end sendPartnerInfoToServer


function sendReqInfoToServer(update){

    url = "/project/addreq/"

     // get all filled in data
    var done = 'False';
    if($('#id_req_done').is(':checked')){
        done = 'True';
    }

    dataToSend = {
        datasetID: datasetID,
        task: $('#id_req_task').val(),
        properties: $('#id_req_properties').val(),
        links: $('#id_req_links').val(),
        partnerID: $("#partnerDataReq").val(),
        deadline: $('#id_req_deadline').val(),
        done: done,
        csrfmiddlewaretoken: csrfmiddlewaretoken}

    if (update == true){
        url = "/project/updatereq/"
        dataToSend['stepID'] = $('#selectedReqID').val();
    }

    $('#selectedReqID').val(-1)
    sendInfoToServer(dataToSend, url, existingReqs, refreshReqs)

} // end sendReqInfoToServer


function sendExpStepInfoToServer(update){

    url = "/project/addstep/"

     // get all filled in data
     var done = 'False';
     if($('#id_exp_done').is(':checked')){
        done = 'True';
     }

    dataToSend = {
        datasetID: datasetID,
        task: $('#id_exp_task').val(),
        properties: $('#id_exp_properties').val(),
        links: $('#id_exp_links').val(),
        partnerID: $("#partnerExpStep").val(),
        deadline: $("#id_exp_deadline").val(),
        done: done,
        csrfmiddlewaretoken: csrfmiddlewaretoken}

    if (update == true){
        url = "/project/updatestep/"
        dataToSend['stepID'] = $('#selectedExpStepID').val();
    }

    $('#selectedExpStepID').val(-1)
    sendInfoToServer(dataToSend, url, existingExpSteps, refreshExpSteps)

} // end sendExpStepInfoToServer


function sendReportingInfoToServer(update){

    url = "/project/addreporting/"

     // get all filled in data
     var done = 'False';
     if($('#id_reporting_done').is(':checked')){
        done = 'True';
     }

    dataToSend = {
        datasetID: datasetID,
        task: $('#id_reporting_task').val(),
        properties: $('#id_reporting_properties').val(),
        links: $('#id_reporting_links').val(),
        partnerID: $("#partnerReporting").val(),
        deadline: $('#id_reporting_deadline').val(),
        done: done,
        csrfmiddlewaretoken: csrfmiddlewaretoken}

    if (update == true){
        url = "/project/updatereporting/"
        dataToSend['stepID'] = $('#selectedReportingID').val();
    }

    $('#selectedReportingID').val(-1)
    sendInfoToServer(dataToSend, url, existingReportings, refreshReporting)

} // end sendReportingInfoToServer


function sendInfoToServer(dataToSend, urlToSend, existingList, refreshFunction){
    /*
    Create an ajax request to update the database. When successful, the updated
    model is send back and a refresh takes place
    */
    $.ajax({
        url: urlToSend,
        type: "POST",
        data: dataToSend,

        // handle a successful response
        success : function(json) {
            existingList = JSON.parse(json['existingListJSON']);
            refreshFunction(existingList);
        },
        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}


function setButtonsReq(active){

    if (active === true){
        $('#updateReqID').removeClass( "disabled" ).addClass( "active" );
        $('#updateReqID').prop( "disabled", false);
        $('#deleteReqID').removeClass( "disabled" ).addClass( "active" );
        $('#deleteReqID').prop( "disabled", false);
        $('#incrTaskNrReqID').removeClass( "disabled" ).addClass( "active" );
        $('#incrTaskNrReqID').prop( "disabled", false);
        $('#decrTaskNrReqID').removeClass( "disabled" ).addClass( "active" );
        $('#decrTaskNrReqID').prop( "disabled", false);
    }
    else{
        $('#updateReqID').removeClass( "active" ).addClass( "disabled" );
        $('#updateReqID').prop( "disabled", true);
        $('#deleteReqID').removeClass( "active" ).addClass( "disabled" );
        $('#deleteReqID').prop( "disabled", true);
        $('#incrTaskNrReqID').removeClass( "active" ).addClass( "disabled" );
        $('#incrTaskNrReqID').prop( "disabled", true);
        $('#decrTaskNrReqID').removeClass( "active" ).addClass( "disabled" );
        $('#decrTaskNrReqID').prop( "disabled", true);
    }
}


function setButtonsExpStep(active){

    if (active === true){
        // update buttons
        $('#updateExpStepID').removeClass( "disabled" ).addClass( "active" );
        $('#updateExpStepID').prop( "disabled", false);
        $('#deleteExpStepID').removeClass( "disabled" ).addClass( "active" );
        $('#deleteExpStepID').prop( "disabled", false);
        $('#incrTaskNrExpStepID').removeClass( "disabled" ).addClass( "active" );
        $('#incrTaskNrExpStepID').prop( "disabled", false);
        $('#decrTaskNrExpStepID').removeClass( "disabled" ).addClass( "active" );
        $('#decrTaskNrExpStepID').prop( "disabled", false);
    }
    else{
        $('#updateExpStepID').removeClass( "active" ).addClass( "disabled" );
        $('#updateExpStepID').prop( "disabled", true);
        $('#deleteExpStepID').removeClass( "active" ).addClass( "disabled" );
        $('#deleteExpStepID').prop( "disabled", true);
        $('#incrTaskNrExpStepID').removeClass( "active" ).addClass( "disabled" );
        $('#incrTaskNrExpStepID').prop( "disabled", true);
        $('#decrTaskNrExpStepID').removeClass( "active" ).addClass( "disabled" );
        $('#decrTaskNrExpStepID').prop( "disabled", true);
    }
}


function setButtonsReporting(active){

    if (active === true){
        $('#updateReportingID').removeClass( "disabled" ).addClass( "active" );
        $('#updateReportingID').prop( "disabled", false);
        $('#deleteReportingID').removeClass( "disabled" ).addClass( "active" );
        $('#deleteReportingID').prop( "disabled", false);
        $('#incrTaskNrReportingID').removeClass( "disabled" ).addClass( "active" );
        $('#incrTaskNrReportingID').prop( "disabled", false);
        $('#decrTaskNrReportingID').removeClass( "disabled" ).addClass( "active" );
        $('#decrTaskNrReportingID').prop( "disabled", false);
    }
    else{
        $('#updateReportingID').removeClass( "active" ).addClass( "disabled" );
        $('#updateReportingID').prop( "disabled", true);
        $('#deleteReportingID').removeClass( "active" ).addClass( "disabled" );
        $('#deleteReportingID').prop( "disabled", true);
        $('#incrTaskNrReportingID').removeClass( "active" ).addClass( "disabled" );
        $('#incrTaskNrReportingID').prop( "disabled", true);
        $('#decrTaskNrReportingID').removeClass( "active" ).addClass( "disabled" );
        $('#decrTaskNrReportingID').prop( "disabled", true);
    }
}

