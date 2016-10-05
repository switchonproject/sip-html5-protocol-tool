__author__ = 'beekhuiz'
from .models import BasicDataset, Partner, DataReq, ExpStep, Reporting
from django.forms.models import model_to_dict
import datetime


def updateLastUpdate(datasetID):
    BasicDataset.objects.filter(id=datasetID).update(
        dateLastUpdate=str(datetime.date.today()))


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
            'shortname': existingExpertimentInfo.shortname,
            'experimentIdea': existingExpertimentInfo.experimentIdea,
            'hypothesis': existingExpertimentInfo.hypothesis,
            'researchObjective': existingExpertimentInfo.researchObjective,
            'dateLastUpdate': str(existingExpertimentInfo.dateLastUpdate),
    }
    return existingExpertimentInfoDict


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

    # store the 'done' checkbox as a boolean
    done = True
    if postDict['done'] == 'False':
        done = False

    if update:
        allObjects.objects.filter(id=postDict['stepID']).update(
            dataset = dataset,
            task=postDict['task'],
            properties=postDict['properties'],
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
            partner = partner,
            deadline=postDict['deadline'],
            done=done
            )

        newObject.save()

    updateLastUpdate(postDict['datasetID'])


def getListSteps(datasetID, allObjects):
    '''
    Store all information in an array list
    :param datasetID: id of the dataset for which the info are retrieved
    :return: list with all Result Reporting information
    '''
    existingObjects = allObjects.objects.filter(dataset__id=datasetID)

    existingObjectsList = []

    for existingObject in existingObjects:

        reportingDict = {
            "id": existingObject.id,
            "taskNr": existingObject.taskNr,
            "task": existingObject.task,
            "properties": existingObject.properties,
            "partnerID": existingObject.partner.id,
            "partnerName": existingObject.partner.name,
            "deadline": str(existingObject.deadline),
            "done": str(existingObject.done),
        }
        existingObjectsList.append(reportingDict)

    # sort on taskNr for better visualisation
    existingObjectsListSorted = sorted(existingObjectsList, key=lambda k: k['taskNr'])

    return existingObjectsListSorted


def getNewTaskNr(datasetID, allObjects):
    '''
    Gets a new task number when a new object is added to the list
    :param datasetID:
    :param allObjects:
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

    datasetObjects = allObjects.objects.filter(dataset__id=datasetID)
    deletedObject = allObjects.objects.get(pk=objectID)

    taskNrToDel = deletedObject.taskNr

    # shift the number of the tasks that come after the task to delete one place up
    for datasetObject in datasetObjects:
        if datasetObject.taskNr > taskNrToDel:
            datasetObject.taskNr -= 1
            datasetObject.save()


def increaseTaskNr(datasetID, objectID, allObjects):

    objectToIncr = allObjects.objects.get(pk=objectID)
    origTaskNr = objectToIncr.taskNr

    if origTaskNr > 1:

        objectToDecr = allObjects.objects.filter(taskNr=origTaskNr-1, dataset__id = datasetID)[0]

        objectToIncr.taskNr = origTaskNr - 1
        objectToIncr.save()

        objectToDecr.taskNr = origTaskNr
        objectToDecr.save()

def decreaseTaskNr(datasetID, objectID, allObjects):

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