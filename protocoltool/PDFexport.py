__author__ = 'beekhuiz'
from .models import BasicDataset, Partner, Publication, DataReq, ExpStep, Reporting
from django.http import HttpResponse
import os
from io import BytesIO

from reportlab.platypus import (
    BaseDocTemplate,
    PageTemplate,
    Frame,
    Paragraph,
    Spacer,
    Table,
    Image,
    TableStyle,
)
from reportlab.lib.units import cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER
from reportlab.lib.colors import Color
from reportlab.lib.colors import (
    black,
)

def writeTasks(story, styles, taskList):
    '''
    :param story: story to which to add the taskList
    :param styles: styling used in the story
    :param taskList: the tasks / steps
    :return: none
    '''
    for task in taskList:

        elem0 = [Paragraph('Task {}:'.format(task.taskNr), styles['label']), Paragraph(task.task.replace('\n','<br />\n').encode('utf8'), styles['default'])]
        elem1 = [Paragraph('Description:', styles['label']), Paragraph(task.properties.replace('\n','<br />\n').encode('utf8'), styles['default'])]
        elem2 = [Paragraph('Links:', styles['label']), Paragraph(task.links.replace('\n','<br />\n').encode('utf8'), styles['default'])]
        elem3 = [Paragraph('Task leader:', styles['label']), Paragraph(task.partner.name.encode('utf8'), styles['default'])]
        elem4 = [Paragraph('Deadline:', styles['label']), Paragraph(str(task.deadline), styles['default'])]

        if (task.links != ""):
            data = [elem0, elem1, elem2, elem3, elem4]
        else:
            data = [elem0, elem1, elem3, elem4]

        t=Table(data, hAlign='LEFT', colWidths=[4 * cm, 12 * cm])
        t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')]))
        story.append(t)
        story.append(Spacer(1, 16))


def createPDF(datasetID):
    """
    Get the ID of the dataset protocol and creates a PDF of this protocol using the reportlab tools
    :param datasetID:
    :return: a HTTPResponse PDF object
    """

    # Get all the information of this protocol
    basicInfo = BasicDataset.objects.get(id=datasetID)
    partnerInfo = Partner.objects.filter(dataset_id=datasetID)
    publicationInfo = Publication.objects.filter(dataset_id=datasetID)
    reqInfo = DataReq.objects.filter(dataset_id=datasetID).order_by('taskNr')
    stepInfo = ExpStep.objects.filter(dataset_id=datasetID).order_by('taskNr')
    reportingInfo = Reporting.objects.filter(dataset_id=datasetID).order_by('taskNr')

    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename=' + basicInfo.shortTitle + '.pdf'

    styles = {
        'default': ParagraphStyle(
            'default',
            fontName='Times-Roman',
            fontSize=10,
            leading=11,
            leftIndent=0,
            rightIndent=0,
            firstLineIndent=0,
            spaceBefore=0,
            spaceAfter=0,
            textColor= black,
            backColor=None,
            wordWrap=None,
            borderWidth= 0,
            borderPadding= 0,
            borderColor= None,
            borderRadius= None,
            allowWidows= 1,
            allowOrphans= 0,
            endDots=None,
            splitLongWords=1,
        ),

    }

    styles['title1'] = ParagraphStyle(
        'title1',
        parent=styles['default'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=30,
        alignment=TA_CENTER,
        textColor=black,
    )

    styles['title2'] = ParagraphStyle(
        'title2',
        parent=styles['default'],
        fontName='Helvetica',
        fontSize=14,
        leading=18,
        leftIndent=5,
        alignment=TA_LEFT,
        textColor=black,
        spaceBefore = 0,
        borderRadius = None,
        firstLineIndent = 0,
        underlineProportion = 0.0,
        rightIndent = 0,
        wordWrap = None,
        allowWidows = 1,
        backColor = Color(.9,.9,.9),
        justifyLastLine = 0,
        textTransform = None,
        justifyBreaks = 0,
        spaceShrinkage = 0.05,
        splitLongWords = 1,
        bulletFontSize = 10,
        borderWidth = 1,
        borderPadding = 2,
        endDots = None,
        spaceAfter = 6,

    )

    styles['label'] = ParagraphStyle(
        'label',
        parent=styles['default'],
        fontName='Times-Bold',
    )

    buffer = BytesIO()
    doc = BaseDocTemplate(buffer)

    doc.addPageTemplates(
        [
            PageTemplate(
                frames=[
                    Frame(
                        doc.leftMargin,
                        doc.bottomMargin,
                        doc.width,
                        doc.height,
                        id=None
                    ),
                ]
            ),
        ]
    )


    # container for the 'Flowable' objects
    story = []

    scriptDir = os.path.dirname(__file__)
    im = Image(os.path.join(scriptDir, "static/img/sologo_new_cropped.png"), width=2.6*cm, height=2*cm)
    im.hAlign = 'RIGHT'

    data = [[im, Paragraph('{}'.format(basicInfo.shortTitle), styles['title1'])]]

    t=Table(data, hAlign='LEFT', colWidths=[2 * cm, 14 * cm])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')]))
    story.append(t)
    story.append(Spacer(1, 16))


    story.append(Paragraph('Experiment Information', styles['title2']))
    data= [[Paragraph('Full experiment name:', styles['label']), Paragraph(basicInfo.title.encode('utf8'), styles['default'])],
           [Paragraph('Experiment Idea:', styles['label']), Paragraph(basicInfo.experimentIdea.replace('\n','<br />\n').encode('utf8'), styles['default'])],
           [Paragraph('Hypothesis:', styles['label']), Paragraph(basicInfo.hypothesis.replace('\n','<br />\n').encode('utf8'), styles['default'])],
           [Paragraph('Research objective:', styles['label']), Paragraph(basicInfo.researchObjective.replace('\n','<br />\n').encode('utf8'), styles['default'])]]

    t=Table(data, hAlign='LEFT', colWidths=[4 * cm, 12 * cm])
    t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')]))
    story.append(t)
    story.append(Spacer(1, 24))


    # Partners
    story.append(Paragraph('Partners', styles['title2']))

    for partner in partnerInfo:
        p = unicode(partner.name)
        partnerName = Paragraph(p, styles['default'])
        if partner.lead == True:
            partnerName = Paragraph('(lead)'+p, styles['default'])

        data = [[Paragraph('Name:', styles['label']), partnerName],
            [Paragraph('E-mail:', styles['label']), Paragraph(partner.email.encode('utf8'), styles['default'])],
           [Paragraph('Organisation:', styles['label']), Paragraph(partner.organisation.encode('utf8'), styles['default'])]]

        t=Table(data, hAlign='LEFT', colWidths=[4 * cm, 12 * cm])
        t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')]))
        story.append(t)
        story.append(Spacer(1, 16))

    story.append(Spacer(1, 24))

    story.append(Paragraph('A) Data & Method Preparation', styles['title2']))
    writeTasks(story, styles, reqInfo)
    story.append(Spacer(1, 24))

    story.append(Paragraph('B) Experiment Analysis Steps', styles['title2']))
    writeTasks(story, styles, stepInfo)
    story.append(Spacer(1, 24))

    story.append(Paragraph('C) Result Reporting', styles['title2']))
    writeTasks(story, styles, reportingInfo)

    # Publications
    story.append(Paragraph('D) Publications', styles['title2']))

    for publication in publicationInfo:

        publicationName = Paragraph('{}'.format(publication.name.encode('utf8')), styles['default'])

        data = [[Paragraph('Paper Title:', styles['label']), publicationName],
           [Paragraph('DOI:', styles['label']), Paragraph(publication.type.encode('utf8'), styles['default'])]]

        t=Table(data, hAlign='LEFT', colWidths=[4 * cm, 12 * cm])
        t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP')]))
        story.append(t)
        story.append(Spacer(1, 16))

    story.append(Spacer(1, 24))

    # write the document to disk
    doc.build(story)

    pdf = buffer.getvalue()
    buffer.close()
    response.write(pdf)
    return response
