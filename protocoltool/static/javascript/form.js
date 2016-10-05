
$(document).ready(function(){

    // fill in all the partner information
    refreshAll();

    $('#partnerTable').on('click', 'tbody tr', function(){

        selectedPartner = $(this).find(".partnername").text();
        $(this).closest("tr").addClass("highlight").siblings().removeClass("highlight");

        var arrayLength = existingPartners.length;


        for (i = 0; i < arrayLength; i++) {

            if(existingPartners[i].name == selectedPartner){

                // set fields to valid
                $('#id_partner_name').removeClass('error');
                $('#id_partner_email').removeClass('error');
                $('#id_partner_organisation').removeClass('error');

                $('#id_partner_lead').prop('checked', false);

                $('#id_partner_name').val(existingPartners[i].name);
                $('#id_partner_email').val(existingPartners[i].email);
                $('#id_partner_organisation').val(existingPartners[i].organisation);

                if(existingPartners[i].lead == 'True'){
                    $('#id_partner_lead').prop('checked', true);
                }
                else{
                    $('#id_partner_lead').prop('checked', false);
                }

                $('#selectedPartnerID').val(existingPartners[i].id);

                // update buttons
                $('#updatePartnerID').removeClass( "disabled" ).addClass( "active" );
                $('#updatePartnerID').prop( "disabled", false);
                $('#deletePartnerID').removeClass( "disabled" ).addClass( "active" );
                $('#deletePartnerID').prop( "disabled", false);
            }
        }
    });


    $('#saveInfoID').on('click', function(){
        /*
        Save the generic experiment info in the database
        */

        // check if all values are valid
        validShortname = checkValidField($('#id_basic_shortname'));
        validTitle = checkValidField($('#id_basic_title'));

        if(validShortname === true && validTitle === true){

            var dataToSend = {
                    shortname: $('#id_basic_shortname').val(),
                    title: $('#id_basic_title').val(),
                    experimentIdea: $('#id_basic_experimentIdea').val(),
                    hypothesis: $('#id_basic_hypothesis').val(),
                    researchObjective: $('#id_basic_researchObjective').val(),
                    datasetID: datasetID,
                    csrfmiddlewaretoken: csrfmiddlewaretoken}

            $.ajax({
                url: "/project/saveexperimentinfo/",
                type: "POST",
                data: dataToSend,

                // handle a successful response
                success : function(json) {
                    existingExperimentInfo = JSON.parse(json['existingExperimentInfoJSON']);
                    refreshExperimentInfo();
                },
                // handle a non-successful response
                error : function(xhr,errmsg,err) {
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                }
            });

        }
        else{
            warningPopup("One or more required fields are filled in incorrectly");
        }
    });


    $('#addPartnerID').on('click', function(){

        removePartnerErrorClasses();

        // check if all values are valid
        validName = checkValidField($('#id_partner_name'));
        validEmail = checkValidField($('#id_partner_email'));
        validOrganisation = checkValidField($('#id_partner_organisation'));

        if(validName === true && validEmail === true && validOrganisation === true){
            sendPartnerInfoToServer(false);
        }
        else{
            warningPopup("One or more fields are filled in incorrectly");
        }
    });

    $('#updatePartnerID').on('click', function(){
        // check if all values are valid
        validName = checkValidField($('#id_partner_name'));
        validEmail = checkValidField($('#id_partner_email'));
        validOrganisation = checkValidField($('#id_partner_organisation'));

        if(validName === true && validEmail === true && validOrganisation === true){
            sendPartnerInfoToServer(true);
        }
        else{
            warningPopup("One or more fields are filled in incorrectly");
        }
    });

    $('#deletePartnerID').on('click', function(){

        var partnerID = $('#selectedPartnerID').val();

        // check if all the partner is not used in the reqs
        partnerUsed = false
        var nrReqs = existingReqs.length;
        for (i = 0; i < nrReqs; i++) {
            if (existingReqs[i].partnerID == partnerID){
                partnerUsed = true;
                warningPopup("This partner is the task leader in the data&method preparation, removal is therefore not allowed.");
            }
        }

        // check if all the partner is not used in the exp steps
        var nrExpSteps = existingExpSteps.length;
        for (i = 0; i < nrExpSteps; i++) {
            if (existingExpSteps[i].partnerID == partnerID){
                partnerUsed = true;
                warningPopup("This partner is a the task leader in the experiment steps, removal is therefore not allowed.")
            }
        }

        if(partnerUsed == false){
            $.ajax({
                url: "/project/deletepartner/",
                type: "POST",
                data: {partnerID: partnerID,
                       datasetID: datasetID,
                       csrfmiddlewaretoken: csrfmiddlewaretoken},

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
        }
    });


    //
    // FUNCTIONS FOR THE DATA REQS
    //

    $('#reqTableID').on('click', 'tbody tr', function(){

        selectedReqID = $(this).closest("tr").attr('id');
        $(this).closest("tr").addClass("highlight").siblings().removeClass("highlight");

        var nrReqs = existingReqs.length;

        for (i = 0; i < nrReqs; i++) {

            if (existingReqs[i].id == selectedReqID){

                removeReqErrorClasses();                // remove all error classes

                $('#id_req_task').val(existingReqs[i].task);
                $('#id_req_properties').val(existingReqs[i].properties);
                $('#id_req_deadline').val(existingReqs[i].deadline);
                if(existingReqs[i].done == 'True'){
                    $('#id_req_done').prop('checked', true);
                }
                else{
                    $('#id_req_done').prop('checked', false);
                }

                contrPartner = getPartnerByID(existingReqs[i].partnerID);

                $('#partnerDataReq').val(contrPartner.id);
                $('#selectedReqID').val(selectedReqID);

                setButtonsReq(true);   // update buttons
            }
        } // end for
    }); // end on reqTable clicked


    $('#addReqID').on('click', function(){

        removeReqErrorClasses();

        // check if all values are valid
        validTask = checkValidField($('#id_req_task'));
        validProp = checkValidField($('#id_req_properties'));
        validPartner = checkValidField($('#partnerDataReq'));
        validDeadline = checkValidField($('#id_req_deadline'));

        if(validTask === true && validProp === true && validPartner === true && validDeadline === true){
            sendReqInfoToServer(false);
        }
        else{
            warningPopup("One or more fields are filled in incorrectly");
        }
    });

    $('#updateReqID').on('click', function(){

        removeReqErrorClasses();

        // check if all values are valid
        validTask = checkValidField($('#id_req_task'));
        validProp = checkValidField($('#id_req_properties'));
        validPartner = checkValidField($('#partnerDataReq'));
        validDeadline = checkValidField($('#id_req_deadline'));

        if(validTask === true && validProp === true && validPartner === true && validDeadline === true){
            sendReqInfoToServer(true);
        }
        else{
            warningPopup("One or more fields are filled in incorrectly");
        }
    });

    $('#deleteReqID').on('click', function(){
        removeReqErrorClasses();

        var dataToSend = {stepID: $('#selectedReqID').val(),
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken}

        sendInfoToServer(dataToSend, "/project/deletereq/", existingReqs, refreshReqs)
    });

    $('#incrTaskNrReqID').on('click', function(){
        var dataToSend = {reqID: $('#selectedReqID').val(),
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken}

        sendInfoToServer(dataToSend, "/project/increasereq/", existingReqs, refreshReqs)
    });

    $('#decrTaskNrReqID').on('click', function(){
        var dataToSend = {reqID: $('#selectedReqID').val(),
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken}

        sendInfoToServer(dataToSend, "/project/decreasereq/", existingReqs, refreshReqs)
    });

    //
    // FUNCTIONS FOR THE STEPS
    //

    $('#expStepTableID').on('click', 'tbody tr', function(){

        selectedExpStepID = $(this).closest("tr").attr('id');
        $(this).closest("tr").addClass("highlight").siblings().removeClass("highlight");

        var nrExpSteps = existingExpSteps.length;

        for (i = 0; i < nrExpSteps; i++) {

            if (existingExpSteps[i].id == selectedExpStepID){

                // remove all error classes
                removeExpErrorClasses();

                $('#id_exp_task').val(existingExpSteps[i].task);
                $('#id_exp_properties').val(existingExpSteps[i].properties);
                $('#id_exp_deadline').val(existingExpSteps[i].deadline);
                if(existingExpSteps[i].done == 'True'){
                    $('#id_exp_done').prop('checked', true);
                }
                else{
                    $('#id_exp_done').prop('checked', false);
                }

                contrPartner = getPartnerByID(existingExpSteps[i].partnerID);

                $('#partnerExpStep').val(contrPartner.id);
                $('#selectedExpStepID').val(selectedExpStepID);

                setButtonsExpStep(true);    // update buttons
            }
        } // end for

    }); // end on expStepTable clicked

    $('#addExpStepID').on('click', function(){

        // check if all values are valid
        validTask = checkValidField($('#id_exp_task'));
        validProp = checkValidField($('#id_exp_properties'));
        validPartner = checkValidField($('#partnerExpStep'));
        validDeadline = checkValidField($('#id_exp_deadline'));

        if(validTask === true && validProp === true && validPartner === true && validDeadline === true){
            sendExpStepInfoToServer(false);
        }
        else{
            warningPopup("One or more fields are filled in incorrectly");
        }
    });

    $('#updateExpStepID').on('click', function(){
        // check if all values are valid
        validTask = checkValidField($('#id_exp_task'));
        validProp = checkValidField($('#id_exp_properties'));
        validPartner = checkValidField($('#partnerExpStep'));
        validDeadline = checkValidField($('#id_exp_deadline'));

        if(validTask === true && validProp === true && validPartner === true && validDeadline === true){
            sendExpStepInfoToServer(true);
        }
        else{
            warningPopup("One or more fields are filled in incorrectly");
        }
    });

    $('#deleteExpStepID').on('click', function(){

         removeExpErrorClasses();

         var dataToSend = {stepID: $('#selectedExpStepID').val(),
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken}

         sendInfoToServer(dataToSend, "/project/deletestep/", existingExpSteps, refreshExpSteps)
    });
    
    $('#incrTaskNrExpStepID').on('click', function(){
        var dataToSend = {expStepID: $('#selectedExpStepID').val(),
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken}

        sendInfoToServer(dataToSend, "/project/increaseexpstep/", existingExpSteps, refreshExpSteps)
    });

    $('#decrTaskNrExpStepID').on('click', function(){
        var dataToSend = {expStepID: $('#selectedExpStepID').val(),
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken}

        sendInfoToServer(dataToSend, "/project/decreaseexpstep/", existingExpSteps, refreshExpSteps)
    });

    
    //
    // FUNCTIONS FOR THE REPORTING
    //

    $('#reportingTableID').on('click', 'tbody tr', function(){

        selectedReportingID = $(this).closest("tr").attr('id');
        $(this).closest("tr").addClass("highlight").siblings().removeClass("highlight");

        var nrReportings = existingReportings.length;

        for (i = 0; i < nrReportings; i++) {

            if (existingReportings[i].id == selectedReportingID){

                removeReportingErrorClasses();                // remove reporting error classes

                $('#id_reporting_task').val(existingReportings[i].task);
                $('#id_reporting_properties').val(existingReportings[i].properties);
                $('#id_reporting_deadline').val(existingReportings[i].deadline);
                if(existingReportings[i].done == 'True'){
                    $('#id_reporting_done').prop('checked', true);
                }
                else{
                    $('#id_reporting_done').prop('checked', false);
                }
                contrPartner = getPartnerByID(existingReportings[i].partnerID);

                $('#partnerReporting').val(contrPartner.id);
                $('#selectedReportingID').val(selectedReportingID);

                setButtonsReporting(true);   // update buttons
            }
        } // end for

    }); // end on reportingTable clicked

    $('#addReportingID').on('click', function(){

        // check if all values are valid
        validTask = checkValidField($('#id_reporting_task'));
        validProp = checkValidField($('#id_reporting_properties'));
        validPartner = checkValidField($('#partnerReporting'));
        validDeadline = checkValidField($('#id_reporting_deadline'));

        if(validTask === true && validProp === true && validPartner === true && validDeadline === true){
            sendReportingInfoToServer(false);
        }
        else{
            warningPopup("One or more fields are filled in incorrectly");
        }
    });

    $('#updateReportingID').on('click', function(){
        // check if all values are valid
        validTask = checkValidField($('#id_reporting_task'));
        validProp = checkValidField($('#id_reporting_properties'));
        validPartner = checkValidField($('#partnerReporting'));
        validDeadline = checkValidField($('#id_reporting_deadline'));

        if(validTask === true && validProp === true && validPartner === true && validDeadline === true){
            sendReportingInfoToServer(true);
        }
        else{
            warningPopup("One or more fields are filled in incorrectly");
        }
    });

    $('#deleteReportingID').on('click', function(){

        removeReportingErrorClasses();

        var dataToSend = {stepID: $('#selectedReportingID').val(),
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken}

        sendInfoToServer(dataToSend, "/project/deletereporting/", existingReportings, refreshReporting)

    });

    $('#incrTaskNrReportingID').on('click', function(){
        var dataToSend = {reportingID: $('#selectedReportingID').val(),
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken}

        sendInfoToServer(dataToSend, "/project/increasereporting/", existingReportings, refreshReporting)
    });

    $('#decrTaskNrReportingID').on('click', function(){
        var dataToSend = {reportingID: $('#selectedReportingID').val(),
                   datasetID: datasetID,
                   csrfmiddlewaretoken: csrfmiddlewaretoken}

        sendInfoToServer(dataToSend, "/project/decreasereporting/", existingReportings, refreshReporting)
    });

});
