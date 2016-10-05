from django.core.urlresolvers import reverse
from django.http import Http404, HttpResponseRedirect
from django.shortcuts import render
from .forms import BasicDatasetForm, PartnerForm, DataReqForm, ExpStepForm, ReportingForm, UserForm, UserProfileForm
from .models import BasicDataset, Partner, DataReq, ExpStep, Reporting, ExternalProtocol
from django.forms.models import model_to_dict
from django.contrib.auth import authenticate, login, logout
import json
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
import datetime
import functions, PDFexport

import pdb

# Django exceptions
from django.core.exceptions import ObjectDoesNotExist


def register(request):

    registered = False

    # If it's a HTTP POST, we're interested in processing form data.
    if request.method == 'POST':
        # Attempt to grab information from the raw form information.
        # Note that we make use of both UserForm and UserProfileForm.
        user_form = UserForm(data=request.POST)
        profile_form = UserProfileForm(data=request.POST)

        # If the two forms are valid...
        if user_form.is_valid() and profile_form.is_valid():
            # Save the user's form data to the database.
            user = user_form.save()

            # Now we hash the password with the set_password method.
            # Once hashed, we can update the user object.
            user.set_password(user.password)
            user.save()

            # Now sort out the UserProfile instance.
            # Since we need to set the user attribute ourselves, we set commit=False.
            # This delays saving the model until we're ready to avoid integrity problems.
            profile = profile_form.save(commit=False)
            profile.user = user

            # Now we save the UserProfile model instance.
            profile.save()

            # Update our variable to tell the template registration was successful.
            registered = True

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal.
        # They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors

    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    # Render the template depending on the context.
    return render(request,
            'protocoltool/register.html',
            {'user_form': user_form, 'profile_form': profile_form, 'registered': registered} )


def user_login(request):

    # If the request is a HTTP POST, try to pull out the relevant information.
    if request.method == 'POST':
        # Gather the username and password provided by the user.
        # This information is obtained from the login form.
                # We use request.POST.get('<variable>') as opposed to request.POST['<variable>'],
                # because the request.POST.get('<variable>') returns None, if the value does not exist,
                # while the request.POST['<variable>'] will raise key error exception
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Use Django's machinery to attempt to see if the username/password
        # combination is valid - a User object is returned if it is.
        user = authenticate(username=username, password=password)

        # If we have a User object, the details are correct.
        # If None (Python's way of representing the absence of a value), no user
        # with matching credentials was found.
        if user:
            # Is the account active? It could have been disabled.
            if user.is_active:
                # If the account is valid and active, we can log the user in.
                # We'll send the user back to the homepage.
                login(request, user)
                return HttpResponseRedirect('/project/participate/')
            else:
                # An inactive account was used - no logging in!
                return HttpResponse("Your ProtocolTool account is disabled.")
        else:
            # Bad login details were provided. So we can't log the user in.
            print "Invalid login details: {0}, {1}".format(username, password)
            return HttpResponse("Invalid login details supplied.")

    # The request is not a HTTP POST, so display the login form.
    # This scenario would most likely be a HTTP GET.
    else:
        # No context variables to pass to the template system, hence the
        # blank dictionary object...
        return render(request, 'protocoltool/login.html', {})

# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):
    # Since we know the user is logged in, we can now just log them out.
    logout(request)

    # Take the user back to the homepage.
    return HttpResponseRedirect('/project/participate/')


def participate(request):
    try:
        dataset_list = BasicDataset.objects.all()

        context = {
            'dataset_list': dataset_list,
            'show_participate': True,
            'show_review': False,
        }

        return render(request, 'protocoltool/protocoloverview.html', context)

    except ObjectDoesNotExist:
        raise Http404


def review(request):
    try:
        dataset_list = BasicDataset.objects.all()
        externalProtocol_list = ExternalProtocol.objects.all()

        context = {
            'dataset_list': dataset_list,
            'external_protocol_list': externalProtocol_list,
            'show_participate': False,
            'show_review': True,
        }

        return render(request, 'protocoltool/protocoloverview.html', context)

    except ObjectDoesNotExist:
        raise Http404


def protocolOverviewAction(request):
    """
    Handle the action buttons pressed on the ProtocolOverview screen
    """

    postDict = request.POST.dict()

    dataset_id = postDict['dataset_id']
    action = postDict['dataset_action']

    dataset_obj = BasicDataset.objects.get(id=dataset_id)

    if action == 'view':
        # go to URL that shows HTML page with all form info
        url = '/view/%s/' % dataset_obj.id
        return HttpResponseRedirect(url)

    if action == 'delete':
        # Remove metadata in database
        BasicDataset.objects.filter(id=dataset_id).delete()

    elif action == 'publish':
        # Fill in dataset published field
        dataset_obj.published = True
        dataset_obj.save()

    elif action == 'unpublish':
        # Empty the dataset published field
        if dataset_obj.published is not None:
            dataset_obj.published = False
            dataset_obj.save()

    elif action == 'export':
        response = PDFexport.createPDF(dataset_id)
        return response

    elif action == 'edit':
        url = '/form/%s/' % dataset_obj.id
        return HttpResponseRedirect(url)

    return HttpResponseRedirect(reverse('protocoltool:protocoloverview_review'))


def createProtocol(request):

    # Create empty dataset
    core_obj = BasicDataset(
        title='',
        shortname='',
        dateLastUpdate=str(datetime.date.today())
    )

    core_obj.save()

    url = '/form/%s/' % core_obj.id
    return HttpResponseRedirect(url)


def viewProtocol(request, dataset_id):
    '''
    Show all information of the protocol
    :param request:
    :param dataset_id: id of the protocol from the post request
    :return:
    '''

    datasetID = int(dataset_id)
    context = getAllProtocolInfo(dataset_id)

    # TEMP: Add partner info from the Partner objects
    #TODO: use partnerinfo in the context to view partner info in the protocol
    context['partners'] = Partner.objects.filter(dataset_id=datasetID)

    return render(request, 'protocoltool/viewprotocol.html', context)


def formAll(request, dataset_id="0"):
    '''
    Open the form for editing
    :param request:
    :param dataset_id: id of the dataset to show the form
    :return:
    '''

    dataset_id = int(dataset_id)

    if request.method == 'GET' and dataset_id != 0:
        context = getAllProtocolInfo(dataset_id)
        return render(request, 'protocoltool/form.html', context)

    elif request.method == 'POST' and dataset_id != 0:
        return HttpResponseRedirect(reverse('protocoltool:protocoloverview_participate'))

    return HttpResponseRedirect(reverse('protocoltool:protocoloverview_participate'))


def getAllProtocolInfo(datasetID):
    '''
    Retrieve all info of a protocol
    :param datasetID: ID of the dataset (protocol) to get all information from
    :return: dictionary with all information of the dataset
    '''

    coreData = BasicDataset.objects.get(id=datasetID)
    formCore = BasicDatasetForm(instance=coreData, auto_id='id_basic_%s')

    # Load in data
    existingExperimentInfoDict = functions.getExperimentInfoDict(datasetID)
    existingPartnersList = functions.getPartnersList(datasetID)
    existingReqsList = functions.getListSteps(datasetID, DataReq)
    existingExpStepsList = functions.getListSteps(datasetID, ExpStep)
    existingReportingsList = functions.getListSteps(datasetID, Reporting)

    formPartner = PartnerForm(auto_id='id_partner_%s')
    formDataReq = DataReqForm(auto_id='id_req_%s')
    formExpStep = ExpStepForm(auto_id='id_exp_%s')
    formReporting = ReportingForm(auto_id='id_reporting_%s')

    formList = [
        ['Basic', formCore],
        ['Partner', formPartner],
        ['DataReq', formDataReq],
        ['ExpStep', formExpStep],
        ['Reporting', formReporting],
    ]

    context = {}

    context.update({
        'edit': True,
        'dataset_id': datasetID,
        'existingExperimentInfoJSON': json.dumps(existingExperimentInfoDict),
        'existingPartnersJSON': json.dumps(existingPartnersList),
        'existingReqsJSON': json.dumps(existingReqsList),
        'existingExpStepsJSON': json.dumps(existingExpStepsList),
        'existingReportingsJSON': json.dumps(existingReportingsList),
        'forms_list': formList
    })

    return context


def saveExperimentInfo(request):

    postDict = request.POST.dict()

    # create new partner object
    BasicDataset.objects.filter(id=postDict['datasetID']).update(
        title=postDict['title'],
        shortname=postDict['shortname'],
        experimentIdea=postDict['experimentIdea'],
        hypothesis=postDict['hypothesis'],
        researchObjective=postDict['researchObjective'],
        checked=True,
        dateLastUpdate=str(datetime.date.today()))

    # convert the basic dataset (=experiment info) to a dictionary
    existingExperimentInfoDict = functions.getExperimentInfoDict(postDict['datasetID'])
    return JsonResponse({'existingExperimentInfoJSON': json.dumps(existingExperimentInfoDict)})


# region PARTNERS
"""
PARTNERS
"""


def addPartner(request):
    postDict = request.POST.dict()

    # update the Partner model based on the post information from the client
    functions.createPartnerModelFromClient(postDict, False)

    # send back the new Partner model as a list to use client side
    existingPartnersList = functions.getPartnersList(postDict['datasetID'])
    return JsonResponse({'existingPartnersJSON': json.dumps(existingPartnersList)})


def updatePartner(request):
    postDict = request.POST.dict()

    # update the Partner model based on the post information from the client
    functions.createPartnerModelFromClient(postDict, True)

    # send back the new Partner model as a list to use client side
    existingPartnersList = functions.getPartnersList(postDict['datasetID'])
    return JsonResponse({'existingPartnersJSON': json.dumps(existingPartnersList)})


def deletePartner(request):
    postDict = request.POST.dict()

    Partner.objects.filter(id=postDict['partnerID']).delete()

    # send back the new Request model as a list to use client side
    existingPartnersList = functions.getPartnersList(postDict['datasetID'])
    return JsonResponse({'existingPartnersJSON': json.dumps(existingPartnersList)})

# endregion


# region DATA PREPARATION
"""
DATA PREPARATION
"""


def addReq(request):
    postDict = request.POST.dict()

    # add a new Request model based on the post information from the client
    functions.createStepModelFromClient(postDict, False, DataReq)

    # send back the new Request model as a list to use client side
    existingReqsList = functions.getListSteps(postDict['datasetID'], DataReq)
    return JsonResponse({'existingListJSON': json.dumps(existingReqsList)})


def updateReq(request):
    postDict = request.POST.dict()

    # update the Request model based on the post information from the client
    functions.createStepModelFromClient(postDict, True, DataReq)

    # send back the new Request model as a list to use client side
    existingReqsList = functions.getListSteps(postDict['datasetID'], DataReq)
    return JsonResponse({'existingListJSON': json.dumps(existingReqsList)})


def deleteReq(request):
    postDict = request.POST.dict()

    functions.updateTaskNrs(postDict['datasetID'], postDict['stepID'], DataReq)

    DataReq.objects.filter(id=postDict['stepID']).delete()

    # send back the new Request model as a list to use client side
    existingReqsList = functions.getListSteps(postDict['datasetID'], DataReq)
    return JsonResponse({'existingListJSON': json.dumps(existingReqsList)})


def increaseReq(request):
    postDict = request.POST.dict()
    functions.increaseTaskNr(postDict['datasetID'], postDict['reqID'], DataReq)

    # send back the new Reqs model as a list to use client side
    existingReqsList = functions.getListSteps(postDict['datasetID'], DataReq)
    return JsonResponse({'existingListJSON': json.dumps(existingReqsList)})


def decreaseReq(request):
    postDict = request.POST.dict()
    functions.decreaseTaskNr(postDict['datasetID'], postDict['reqID'], DataReq)

    # send back the new Reqs model as a list to use client side
    existingReqsList = functions.getListSteps(postDict['datasetID'], DataReq)
    return JsonResponse({'existingListJSON': json.dumps(existingReqsList)})


# endregion


# region EXPERIMENT STEPS
"""
EXPERIMENT STEPS
"""


def addExpStep(request):
    postDict = request.POST.dict()

    # add a new ExpStep model based on the post information from the client
    functions.createStepModelFromClient(postDict, False, ExpStep)

    # send back the new ExpSteps model as a list to use client side
    existingExpStepsList = functions.getListSteps(postDict['datasetID'], ExpStep)
    return JsonResponse({'existingListJSON': json.dumps(existingExpStepsList)})


def updateExpStep(request):
    postDict = request.POST.dict()

    # update the ExpStep model based on the post information from the client
    functions.createStepModelFromClient(postDict, True, ExpStep)

    # send back the new ExpSteps model as a list to use client side
    existingExpStepsList = functions.getListSteps(postDict['datasetID'], ExpStep)
    return JsonResponse({'existingListJSON': json.dumps(existingExpStepsList)})


def deleteExpStep(request):
    postDict = request.POST.dict()

    functions.updateTaskNrs(postDict['datasetID'], postDict['stepID'], ExpStep)

    ExpStep.objects.filter(id=postDict['stepID']).delete()

    # send back the new ExpSteps model as a list to use client side
    existingExpStepsList = functions.getListSteps(postDict['datasetID'], ExpStep)
    return JsonResponse({'existingListJSON': json.dumps(existingExpStepsList)})


def increaseExpStep(request):
    postDict = request.POST.dict()
    functions.increaseTaskNr(postDict['datasetID'], postDict['expStepID'], ExpStep)

    # send back the new ExpSteps model as a list to use client side
    existingExpStepsList = functions.getListSteps(postDict['datasetID'], ExpStep)
    return JsonResponse({'existingListJSON': json.dumps(existingExpStepsList)})


def decreaseExpStep(request):
    postDict = request.POST.dict()
    functions.decreaseTaskNr(postDict['datasetID'], postDict['expStepID'], ExpStep)

    # send back the new ExpSteps model as a list to use client side
    existingExpStepsList = functions.getListSteps(postDict['datasetID'], ExpStep)
    return JsonResponse({'existingListJSON': json.dumps(existingExpStepsList)})

# endregion


#region REPORTING STEPS
"""
REPORTING STEPS
"""


def addReporting(request):
    postDict = request.POST.dict()

    # add a new Reporting model based on the post information from the client
    functions.createStepModelFromClient(postDict, False, Reporting)

    # send back the new Reportings model as a list to use client side
    existingReportingsList = functions.getListSteps(postDict['datasetID'], Reporting)
    return JsonResponse({'existingListJSON': json.dumps(existingReportingsList)})


def updateReporting(request):
    postDict = request.POST.dict()

    # update the Reporting model based on the post information from the client
    functions.createStepModelFromClient(postDict, True, Reporting)

    # send back the new Reportings model as a list to use client side
    existingReportingsList = functions.getListSteps(postDict['datasetID'], Reporting)
    return JsonResponse({'existingListJSON': json.dumps(existingReportingsList)})


def deleteReporting(request):
    postDict = request.POST.dict()

    functions.updateTaskNrs(postDict['datasetID'], postDict['stepID'], Reporting)
    Reporting.objects.filter(id=postDict['stepID']).delete()

    # send back the new Reportings model as a list to use client side
    existingReportingsList = functions.getListSteps(postDict['datasetID'], Reporting)
    return JsonResponse({'existingListJSON': json.dumps(existingReportingsList)})


def increaseReporting(request):
    postDict = request.POST.dict()
    functions.increaseTaskNr(postDict['datasetID'], postDict['reportingID'], Reporting)

    # send back the new Reportings model as a list to use client side
    existingReportingsList = functions.getListSteps(postDict['datasetID'], Reporting)
    return JsonResponse({'existingListJSON': json.dumps(existingReportingsList)})


def decreaseReporting(request):
    postDict = request.POST.dict()
    functions.decreaseTaskNr(postDict['datasetID'], postDict['reportingID'], Reporting)

    # send back the new Reportings model as a list to use client side
    existingReportingsList = functions.getListSteps(postDict['datasetID'], Reporting)
    return JsonResponse({'existingListJSON': json.dumps(existingReportingsList)})

# endregion
