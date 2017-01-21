__author__ = 'beekhuiz'
from .forms import BasicDatasetForm, PartnerForm, PublicationForm, DataReqForm, ExpStepForm, ReportingForm, UserForm, UserProfileForm
from .models import UserProfile, BasicDataset, Partner, Publication, DataReq, ExpStep, Reporting
from django.core.mail import send_mail
import datetime
import json


def sendEmailConfirmationEditRights(request, datasetID, userProfile):
    '''
    :param request: all request info; needed to retrieve the URL of the page that can now be edited
    :param datasetID: id of the dataset (= protocol) for which editing rights are given
    :param userProfile: the userprofile information of the person that has gained editing rights
    :return: a message stating if an email was send succesfully to the person gaining editing rights
    '''
    coreData = BasicDataset.objects.get(id=datasetID)
    leadUser = coreData.leadUser
    form_link = 'http://' + request.META['HTTP_HOST'] + "/form/" + str(datasetID)

    # send an email
    htmlMessage = "<p>Dear " + userProfile.user.username + ',<br>' + \
                  str(leadUser) + " has given you the rights to edit the protocol " + coreData.shortTitle + ".<br>" + "Please click " + \
                  "<a href=\""+form_link+"\">HERE</a> to start editing the protocol.<br><br></p>"

    nrMessagesSend = send_mail(subject="Edit rights granted for " + coreData.shortTitle, message="",
                               from_email="switchon.vwsl@gmail.com", recipient_list=[str(userProfile.user.email)],
                               html_message=htmlMessage)

    if nrMessagesSend == 1:
        returnMessage = str(leadUser) + ' has given ' + str(userProfile.user.username) + " rights to edit the protocol " + coreData.shortTitle + ". " + \
                        "An email has been sent to " + str(userProfile.user) + " (" + str(userProfile.user.email) + ")" + " to inform about the new edit rights."
    else:
        returnMessage = str(leadUser) + ' has given ' + str(userProfile.user.username) + " rights to edit the protocol " + coreData.shortTitle + ". " + \
                        "There was an error in sending an email to " + str(userProfile.user) + " (" + str(userProfile.user.email) + ")" + " to inform about the new edit rights."

    return returnMessage



def getProtocolInfoInJSON(datasetID):
    '''
    Retrieve all info of a protocol in JSON format, which can be easily read by javascript
    :param datasetID: ID of the dataset (protocol) to get all information from
    :return: dictionary with all information of the dataset
    '''

    # Load in data
    experimentInfoDict = getExperimentInfoDict(datasetID)
    partnersList = getPartnersList(datasetID)
    publicationsList = getPublicationsList(datasetID)
    reqsList = getListSteps(datasetID, DataReq)
    expStepsList = getListSteps(datasetID, ExpStep)
    reportingsList = getListSteps(datasetID, Reporting)

    context = {}
    context.update({
        'edit': True,
        'datasetID': datasetID,
        'experimentInfoJSON': json.dumps(experimentInfoDict),
        'partnersJSON': json.dumps(partnersList),
        'publicationsJSON': json.dumps(publicationsList),
        'reqsJSON': json.dumps(reqsList),
        'expStepsJSON': json.dumps(expStepsList),
        'reportingsJSON': json.dumps(reportingsList),
    })

    return context


def getAllFormInfo(datasetID):
    '''
    :param datasetID: ID of the dataset (protocol) to get all information from
    :return: a list of Django forms that are used to create the form HTML-page
    '''
    coreData = BasicDataset.objects.get(id=datasetID)
    formCore = BasicDatasetForm(instance=coreData, auto_id='id_basic_%s')

    formPartner = PartnerForm(auto_id='id_partner_%s')
    formDataReq = DataReqForm(auto_id='id_req_%s')
    formExpStep = ExpStepForm(auto_id='id_exp_%s')
    formReporting = ReportingForm(auto_id='id_reporting_%s')
    formPublication = PublicationForm(auto_id='id_publication_%s')
    formList = [
        ['Basic', formCore],
        ['Partner', formPartner],
        ['DataReq', formDataReq],
        ['ExpStep', formExpStep],
        ['Reporting', formReporting],
        ['Publication', formPublication],
    ]

    return formList


def updateLastUpdate(datasetID):
    BasicDataset.objects.filter(id=datasetID).update(
        dateLastUpdate=str(datetime.date.today()))

def createPublicationModelFromClient(postDict, update):
    '''
    Creates a new data Publication model object using an AJAX call from the client
    :param postDict: information of the Partner from the client
    :param update: boolean indicating whether it is an update or an addition
    :return: none
    '''

    # get the foreign key of the protocol dataset of this partner
    dataset = BasicDataset.objects.get(id=postDict['datasetID'])

    if update:
        Publication.objects.filter(id=postDict['publicationID']).update(
        name=postDict['name'],
        type=postDict['type'])
    else:
        # create new partner object
        publicationObj = Publication(
            dataset = dataset,
            name=postDict['name'],
            type=postDict['type']
        )
        publicationObj.save()

    updateLastUpdate(postDict['datasetID'])

def createPartnerModelFromClient(postDict, update):
    '''
    Creates a new data Partner model object using an AJAX call from the client
    :param postDict: information of the Partner from the client
    :param update: boolean indicating whether it is an update or an addition
    :return: none
    '''

    # get the foreign key of the protocol dataset of this partner
    dataset = BasicDataset.objects.get(id=postDict['datasetID'])

    # store the lead as a boolean
    lead = True
    if postDict['lead'] == 'False':
        lead = False

    if update:
        Partner.objects.filter(id=postDict['partnerID']).update(
        name=postDict['name'],
        email=postDict['email'],
        organisation=postDict['organisation'],
        lead=lead)
    else:
        # create new partner object
        partnerObj = Partner(
            dataset = dataset,
            name=postDict['name'],
            email=postDict['email'],
            organisation=postDict['organisation'],
            lead=lead
            )
        partnerObj.save()

    updateLastUpdate(postDict['datasetID'])


def getExperimentInfoDict(datasetID):
    '''
    Store all experiment information in a dictionary
    :param datasetID: id of the dataset for which the partners are retrieved
    :return: dictionary of experiment info
    '''

    existingExpertimentInfo = BasicDataset.objects.get(id=datasetID)

    existingExpertimentInfoDict = {
            'title': existingExpertimentInfo.title,
            'shortTitle': existingExpertimentInfo.shortTitle,
            'experimentIdea': existingExpertimentInfo.experimentIdea,
            'hypothesis': existingExpertimentInfo.hypothesis,
            'researchObjective': existingExpertimentInfo.researchObjective,
            'dateLastUpdate': str(existingExpertimentInfo.dateLastUpdate),
    }
    return existingExpertimentInfoDict

def getPublicationsList(datasetID):
    '''
    Store all publication information in an array list
    :param datasetID: id of the dataset for which the publication are retrieved
    :return: list with all publication
    '''

    existingPublications = Publication.objects.filter(dataset__id=datasetID)

    existingPublicationsList = []
    for publication in existingPublications:
        publicationDict = {
            "id": publication.id,
            "name": publication.name,
            "type": publication.type,
        }
        existingPublicationsList.append(publicationDict)

    return existingPublicationsList

def getPartnersList(datasetID):
    '''
    Store all partner information in an array list
    :param datasetID: id of the dataset for which the partners are retrieved
    :return: list with all partners
    '''

    existingPartners = Partner.objects.filter(dataset__id=datasetID)

    existingPartnersList = []
    for partner in existingPartners:
        partnerDict = {
            "id": partner.id,
            "name": partner.name,
            "email": partner.email,
            "organisation": partner.organisation,
            "lead": str(partner.lead),
        }
        existingPartnersList.append(partnerDict)

    return existingPartnersList


def createStepModelFromClient(postDict, update, allObjects):
    '''
    Creates a new Result Reporting  model object using an AJAX call from the client
    :param postDict: information of the Result Reporting step from the client
    :param update: boolean indicating whether it is an update or an addition
    :return: none
    '''

    dataset = BasicDataset.objects.get(id=postDict['datasetID'])
    partner = Partner.objects.get(id=postDict['partnerID'])

    # convert the 'done' checkbox to a boolean
    done = True
    if postDict['done'] == 'False':
        done = False

    # Non mandatory field links
    if 'links' in postDict.keys():
        links = postDict['links']
    else:
        links = ''

    if update:
        allObjects.objects.filter(id=postDict['stepID']).update(
            dataset = dataset,
            task=postDict['task'],
            properties=postDict['properties'],
            links=links,
            partner = partner,
            deadline=postDict['deadline'],
            done=done
            )
    else:
        # create new exp step object
        newObject = allObjects(
            dataset = dataset,
            task=postDict['task'],
            taskNr=getNewTaskNr(postDict['datasetID'], allObjects),
            properties=postDict['properties'],
            links=links,
            partner = partner,
            deadline=postDict['deadline'],
            done=done
            )

        newObject.save()

    updateLastUpdate(postDict['datasetID'])


def getListSteps(datasetID, allObjects):

    '''
    Convert Django objects to a sorted list of dictionaries for use in the form
    :param datasetID: id of the dataset for which the info are retrieved
    :param allObjects: the objects (i.e. DataReq, ExpSteps or Reportings) that are converted to a list of dics
    :return: sorted list if dictionaries of all objects
    '''

    existingObjects = allObjects.objects.filter(dataset__id=datasetID)
    existingObjectsList = []

    for existingObject in existingObjects:

        objectDict = {
            "id": existingObject.id,
            "taskNr": existingObject.taskNr,
            "task": existingObject.task,
            "properties": existingObject.properties,
            "links": existingObject.links,
            "partnerID": existingObject.partner.id,
            "partnerName": existingObject.partner.name,
            "deadline": str(existingObject.deadline),
            "done": str(existingObject.done),
        }

        existingObjectsList.append(objectDict)

    # sort on taskNr for better visualisation
    existingObjectsListSorted = sorted(existingObjectsList, key=lambda k: k['taskNr'])

    return existingObjectsListSorted


def getNewTaskNr(datasetID, allObjects):
    '''
    Gets a new task number when a new object is added to the list
    :param datasetID: id of the dataset (=protocol)
    :param allObjects: the objects (i.e. DataReq, ExpSteps or Reportings)
    :return: highest task number + 1
    '''
    datasetObjects = allObjects.objects.filter(dataset__id=datasetID)

    taskNrs = []

    for datasetObject in datasetObjects:
        taskNrs.append(datasetObject.taskNr)

    # check if there are already tasks defined; if not, task nr is 1
    if len(taskNrs) > 0:
        return max(taskNrs) + 1
    else:
        return 1


def updateTaskNrs(datasetID, objectID, allObjects):
    '''
    Update the task numbers when a step is deleted
    :param datasetID: id of the dataset (=protocol)
    :param objectID: the id of the object
    :param allObjects: the objects (i.e. DataReq, ExpSteps or Reportings)
    :return: none
    '''

    datasetObjects = allObjects.objects.filter(dataset__id=datasetID)
    deletedObject = allObjects.objects.get(pk=objectID)

    taskNrToDel = deletedObject.taskNr

    # shift the number of the tasks that come after the task to delete one place up
    for datasetObject in datasetObjects:
        if datasetObject.taskNr > taskNrToDel:
            datasetObject.taskNr -= 1
            datasetObject.save()


def increaseTaskNr(datasetID, objectID, allObjects):
    '''
    Move task one position (task nr) up; thus decrease the task nr. This means that the other task needs to increase the task nr.
    :param datasetID: id of the dataset (=protocol)
    :param objectID: the id of the object
    :param allObjects: the objects (i.e. DataReq, ExpSteps or Reportings)
    :return: none
    '''

    objectToIncr = allObjects.objects.get(pk=objectID)
    origTaskNr = objectToIncr.taskNr

    if origTaskNr > 1:

        objectToDecr = allObjects.objects.filter(taskNr=origTaskNr-1, dataset__id = datasetID)[0]

        objectToIncr.taskNr = origTaskNr - 1
        objectToIncr.save()

        objectToDecr.taskNr = origTaskNr
        objectToDecr.save()


def decreaseTaskNr(datasetID, objectID, allObjects):
    '''
    Move task one position (task nr) down; thus increase the task nr. This means that the other task needs to decrease the task nr.
    :param datasetID: id of the dataset (=protocol)
    :param objectID: the id of the object
    :param allObjects: the objects (i.e. DataReq, ExpSteps or Reportings)
    :return: none
    '''

    objectToDecr = allObjects.objects.get(pk=objectID)
    origTaskNr = objectToDecr.taskNr

    # get all tasknrs to check if it is the lowest task
    datasetObjects = allObjects.objects.filter(dataset__id=datasetID)
    taskNrs = []

    for datasetObject in datasetObjects:
        taskNrs.append(datasetObject.taskNr)

    if origTaskNr < max(taskNrs):

        objectToIncr = allObjects.objects.filter(taskNr=origTaskNr+1, dataset__id = datasetID)[0]

        objectToDecr.taskNr = origTaskNr + 1
        objectToDecr.save()

        objectToIncr.taskNr = origTaskNr
        objectToIncr.save()