from django.core.urlresolvers import reverse
from django.core.mail import send_mail
from django.shortcuts import render
from .forms import UserForm, UserProfileForm
from .models import UserProfile, BasicDataset, Partner, DataReq, ExpStep, Reporting, ExternalProtocol
from django.contrib.auth import authenticate, login, logout
from django.contrib.messages import error
import json
from django.http import JsonResponse, HttpResponseRedirect, HttpResponse
from django.contrib.auth.decorators import login_required
import datetime
import functions, PDFexport
import base64


def grantEditRights(request):
    '''
    Give edit rights based on an encoded get parameter
    :param request: used to retrieve HTTP address of the server and the get request parameter
    :return: a confirmation if granting the editing rights was successful
    '''
    if request.method == 'GET':

        requestDict = dict(request.GET)

        if 'info' in requestDict.keys():
            editInfo = base64.urlsafe_b64decode(str(requestDict['info'][0]))

            datasetID = int(editInfo.split(",")[0])
            coreData = BasicDataset.objects.get(id=datasetID)

            userID = int(editInfo.split(",")[1])

            for userProfile in UserProfile.objects.all():
                if userProfile.user.id == userID:
                    coreData.editUsers.add(userProfile)

                    # send an email
                    returnMessage = functions.sendEmailConfirmationEditRights(request, datasetID, userProfile)
                    return HttpResponse(returnMessage)

    return HttpResponse('Error in granting editing rights. Please contact switchon.vwsl@gmail.com for assistance.')


def register(request):
    '''
    Register a new user
    :param request: contains form information used to create a new userProfile
    :return: message stating if registering was successful
    '''


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
            profile.save()

            # Login after registration
            user_login(request)

            return HttpResponseRedirect('/project/participate/')


        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal. They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors
            return HttpResponse("Invalid registration: " + str(user_form.errors) + ", "  + str(profile_form.errors))


    # Not a HTTP POST, so we render our form using two ModelForm instances.
    # These forms will be blank, ready for user input.
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

        return render(request,
                'protocoltool/register.html',
                {'user_form': user_form, 'profile_form': profile_form} )


def user_login(request):
    '''
    Log in to the protocol tool
    :param request: contains login info
    :return: redirect to the participate overview; if login failed, give HTTP error message
    '''

    if request.method == 'POST':
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
            # DEBUG: print "Invalid login details: {0}, {1}".format(username, password)
            response_html="""
            <!DOCTYPE html><html><body><p><b>
            Invalid login details supplied.</b><br/>
            Please click on the following link if you have forgotten your credentials:
            <a href="mailto:switchon.vwsl@gmail.com?Subject=Forgotten password" target="_top">Send Mail</a>
            </p></body></html>
            """
            return HttpResponse(response_html)

    # The request is not a HTTP POST, so display the login form.
    else:
        # No context variables to pass to the template system, just go back to main page
        return HttpResponseRedirect('/project/participate/')


# Use the login_required() decorator to ensure only those logged in can access the view.
@login_required
def user_logout(request):

    logout(request)    # Since we know the user is logged in, we can now just log them out.
    return HttpResponseRedirect('/project/participate/')


def participate(request):
    '''
    Show the protocols which are ongoing, so in which the user could participate.
    This function also handles actions of the participate page, which are recognized by a POST with a 'datasetAction'
    :param request
    :return: rendering of the protocoloverview web page
    '''

    # check if an action button has been pressed
    if request.method == 'POST':
        postDict = request.POST.dict()
        if 'datasetAction' in postDict.keys():
            return protocolOverviewAction(request)

    datasetList = BasicDataset.objects.all()

    # create a list of the ids of all users that can edit the datasets; use the ID of the user (not the userprofile!)
    for dataset in datasetList:
        idList = []
        for editUser in dataset.editUsers.all():
            idList.append(editUser.user.id)
        dataset.editUserIds = idList

    context = {
        'datasetList': datasetList,
        'showParticipate': True,
        'showReview': False,
    }

    return render(request, 'protocoltool/protocoloverview.html', context)


def review(request):
    '''
    Show the protocols which are finished
    This function also handles actions of the review page, which are recognized by a POST with a 'datasetAction'
    :param request
    :return: rendering of the protocoloverview web page
    '''

    # check if an action button has been pressed
    if request.method == 'POST':
        postDict = request.POST.dict()
        if 'datasetAction' in postDict.keys():
            return protocolOverviewAction(request)

    datasetList = BasicDataset.objects.all()
    externalProtocolList = ExternalProtocol.objects.all()

    context = {
        'datasetList': datasetList,
        'externalProtocolList': externalProtocolList,
        'showParticipate': False,
        'showReview': True,
    }

    return render(request, 'protocoltool/protocoloverview.html', context)


def protocolOverviewAction(request):
    """
    Handle the action buttons pressed on the ProtocolOverview screen
    """

    postDict = request.POST.dict()

    datasetID = postDict['datasetID']
    action = postDict['datasetAction']
    coreData = BasicDataset.objects.get(id=datasetID)

    if action == 'view':
        # go to URL that shows HTML page with all form info
        url = '/view/%s/' % coreData.id
        return HttpResponseRedirect(url)

    elif action == 'deleteProtocol':
        # set the hidden = True
        coreData.hidden = True
        coreData.save()


    elif action == 'publish':
        # Fill in dataset published field
        coreData.published = True
        coreData.save()
        return HttpResponseRedirect('/project/review/')

    elif action == 'unpublish':
        # Empty the dataset published field
        if coreData.published is not None:
            coreData.published = False
            coreData.save()

    elif action == 'export':
        response = PDFexport.createPDF(datasetID)
        return response

    elif action == 'edit':
        url = '/form/%s/' % coreData.id
        return HttpResponseRedirect(url)

    elif action == 'requestEdit':
        leadName = str(coreData.leadUser.user)
        leadEmail = str(coreData.leadUser.user.email)

        alertMessage = ""

        if request.user.is_authenticated():
            username = request.user.username
            stringToEncode = str(datasetID) + "," + str(request.user.id)
            encodedEditRequest = base64.urlsafe_b64encode(stringToEncode)

            htmlMessage = "<p>Dear " + leadName + ',<br>' + \
            username + " wants to edit the protocol " + coreData.shortTitle + ".<br>" + "Please click " + \
            "<a href='" + request.META['HTTP_HOST'] + "/" + "granteditrights/?info=" + \
            encodedEditRequest + "'>HERE</a> to authorize " + username + " to edit the protocol. <br><br></p>"

            nrMessagesSend = send_mail(subject="Request for edit rights Protocol Tool", message="", from_email="switchon.vwsl@gmail.com", recipient_list=[leadEmail], html_message=htmlMessage)

            if nrMessagesSend > 0:
                alertMessage = "An email has been sent to " + leadName + " (" + leadEmail + ") to request edit rights."
            elif nrMessagesSend == 0:
                alertMessage = "Could not send a message to " + leadName + " (" + leadEmail + "). Please contact switchon.vwsl@gmail.com."

        else:      # user is not logged in
            alertMessage = "Please log in first to send a message"

        error(request, alertMessage)                    # use the message framework to send a message to the participate view
        return HttpResponseRedirect('/participate/')    # a HttpResponse must be given as a result of the form post

    elif action == 'userAdmin':
        url = '/useradmin/%s/' % coreData.id
        return HttpResponseRedirect(url)

    return HttpResponseRedirect('/project/participate/')


def userAdmin(request, datasetID):
    '''
    :param request:
    :param datasetID: id of the dataset (=Protocol)
    :return: render the web page of the user admin page
    '''

    context = {}
    context['datasetID'] = datasetID

    try:
        coreData = BasicDataset.objects.get(id=datasetID)
    except:
        return HttpResponse('<h2>The protocol with ID ' + str(datasetID) + " cannot be found</h2>")

    if request.method == 'POST':
        postDict = request.POST.dict()

        if "select_add" in postDict.keys():
            # add a user
            userToAdd = postDict["select_add"]

            for userProfile in UserProfile.objects.all():
                if userProfile.user.username == userToAdd:
                    coreData.editUsers.add(userProfile)
                    returnMessage = functions.sendEmailConfirmationEditRights(request, datasetID, userProfile)
                    error(request, returnMessage)  # use the message framework to send a message to the useradmin view


        if "select_remove" in postDict.keys():
            # remove a user
            userToRemove = postDict["select_remove"]

            for userProfile in UserProfile.objects.all():
                if userProfile.user.username == userToRemove:
                    coreData.editUsers.remove(userProfile)

        url = '/useradmin/%s/' % datasetID
        return HttpResponseRedirect(url)

    if request.method == 'GET':
        context['shortTitle'] = coreData.shortTitle

        editUsers = []
        editUsersNames = []
        for editUser in coreData.editUsers.all():
            editUsers.append(editUser)
            editUsersNames.append(editUser.user.username)
        context['edit_users'] = editUsers

        # get the list of non-edit users
        nonEditUsers = []
        for userProfile in UserProfile.objects.all():
            if userProfile.user.username not in editUsersNames:
                nonEditUsers.append(userProfile)
        context['non_edit_users'] = nonEditUsers

        return render(request, 'protocoltool/useradmin.html', context)


def registerOrLoginCreateProtocol(request):
    '''
    Create a new protocol. If not logged in already, open a page to either register or login.
    After filling in the registration info or the login info, a new protocol is made.
    :param request:
    :return:
    '''

    # check if user is already logged in; if yes, immediately create protocol
    if request.user.is_authenticated():
        return createProtocol(request)
    else:
        # open the register or login page
        user_form = UserForm()
        profile_form = UserProfileForm()

        return render(request,
                      'protocoltool/createprotocol.html',
                      {'user_form': user_form, 'profile_form': profile_form})


def loginAndCreateProtocol(request):
    '''
    First login (check for valid credentials) and then create protocol.
    TODO: this code is almost the same as the login procedure, could be merged / made more efficient?
    '''

    username = request.POST.get('username')
    password = request.POST.get('password')

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
            return createProtocol(request)      # TODO: Only line that is different from other login procedure
        else:
            # An inactive account was used - no logging in!
            return HttpResponse("Your ProtocolTool account is disabled.")
    else:
        # Bad login details were provided. So we can't log the user in.
        # DEBUG: print "Invalid login details: {0}, {1}".format(username, password)
        response_html = """
             <!DOCTYPE html><html><body><p><b>
             Invalid login details supplied.</b><br/>
             Please click on the following link if you have forgotten your credentials:
             <a href="mailto:switchon.vwsl@gmail.com?Subject=Forgotten password" target="_top">Send Mail</a>
             </p></body></html>
             """
        return HttpResponse(response_html)




def registerAndCreateProtocol(request):
    '''
    Register a new user and create a new protocol afterwards
    TODO: this code is almost the same as the register procedure, could be merged / made more efficient?
    :param request: contains form information used to create a new userProfile
    :return: message stating if registering was successful
    '''

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
            profile.save()

            # Login after registration
            user_login(request)

            return createProtocol(request)

        # Invalid form or forms - mistakes or something else?
        # Print problems to the terminal. They'll also be shown to the user.
        else:
            print user_form.errors, profile_form.errors
            return HttpResponse("Invalid registration: " + str(user_form.errors) + ", " + str(profile_form.errors))



def createProtocol(request):
    '''
    Creates a new empty protocol (is still hidden; will be made visible if user presses the save button in the edit form..
    else there will be many empty but visible protocols in the participate overview)
    :param request:
    :return: to the edit form (or message what went wrong in creating the protocol)
    '''
    if request.user.is_authenticated():

        # Create empty dataset
        basicDataset = BasicDataset(
            title='',
            shortTitle='',
            leadUser=UserProfile.objects.get(user=request.user),
            hidden=True,
            dateLastUpdate=str(datetime.date.today())
        )

        basicDataset.save()
        url = '/form/%s/' % basicDataset.id
        return HttpResponseRedirect(url)

    else:
        return HttpResponse("Please log in first")


def viewProtocol(request, datasetID):
    '''
    Show all information of the protocol
    '''

    try:
        context = functions.getProtocolInfoInJSON(datasetID)

        # get the short title as a separate attribute for easy templating in the html
        basicInfo = BasicDataset.objects.get(id=datasetID)
        context['shortTitle'] = basicInfo.shortTitle
        context['partners'] = Partner.objects.filter(dataset_id=datasetID)
    except:
        return HttpResponse('<h2>The protocol with ID ' + str(datasetID) + " cannot be found</h2>")


    return render(request, 'protocoltool/viewprotocol.html', context)


# @login_required
def formAll(request, datasetID="0"):
    '''
    Open the form for editing
    '''

    # check if user has editing rights
    if request.user.is_authenticated():
        username = request.user.username

        # get all the user names that have edit rights
        try:
            coreData = BasicDataset.objects.get(id=datasetID)
        except:
            return HttpResponse('<h2>The protocol with ID ' + str(datasetID) + " cannot be found</h2>")

        nameList = []
        for editUser in coreData.editUsers.all():
            nameList.append(editUser.user.username)

        # add the leaduser to the namelist (always has rights to edit)
        nameList.append(coreData.leadUser.user.username)

        if username in nameList:
            if request.method == 'GET' and datasetID != 0:
                context = functions.getProtocolInfoInJSON(datasetID)
                context['forms_list'] = functions.getAllFormInfo(datasetID)

                return render(request, 'protocoltool/form.html', context)

            elif request.method == 'POST' and datasetID != 0:
                return HttpResponseRedirect(reverse('protocoltool:protocoloverview_participate'))
        else:
            return HttpResponse("You do not have permission to edit this protocol")
    else:
        return HttpResponse("Please log in to edit this protocol")

    return HttpResponseRedirect(reverse('protocoltool:protocoloverview_participate'))


def saveExperimentInfo(request):

    postDict = request.POST.dict()

    # create new partner object
    BasicDataset.objects.filter(id=postDict['datasetID']).update(
        title=postDict['title'],
        shortTitle=postDict['shortTitle'],
        experimentIdea=postDict['experimentIdea'],
        hypothesis=postDict['hypothesis'],
        researchObjective=postDict['researchObjective'],
        hidden=False,
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