from django import forms
from .models import BasicDataset, Partner, DataReq, ExpStep, Reporting, UserProfile
from django.forms.widgets import DateInput, Textarea, TextInput, EmailInput
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['website']


class BasicDatasetForm(forms.ModelForm):
    class Meta:
        model = BasicDataset
        fields = [
            'title',
            'shortname',
            'experimentIdea',
            'hypothesis',
            'researchObjective',
        ]
        labels = {
            'title': 'Full name',
            'shortname': 'Short name',
            'experimentIdea': 'Experiment Idea',
            'hypothesis' : 'Hypothesis',
            'researchObjective': 'Research Objective',
        }
        widgets = {
            'title': TextInput(
                attrs={'class': 'form-control input-sm', 'autofocus': 'autofocus'}
            ),
            'shortname': TextInput(
                attrs={'class': 'form-control input-sm', 'autofocus': 'autofocus'}
            ),
            'experimentIdea': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm'}
            ),
            'hypothesis': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm'}
            ),
            'researchObjective': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm'}
            )
        }


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = [
            'name',
            'email',
            'organisation',
            'lead',
        ]

        widgets = {
            'name': TextInput(
                attrs={'class': 'form-control input-sm', 'autofocus': 'autofocus'}
            ),
            'email': EmailInput(
                attrs={'class': 'form-control input-sm'}
            ),
            'organisation': TextInput(
                attrs={'class': 'form-control input-sm'}
            ),
        }


class DataReqForm(forms.ModelForm):
    class Meta:
        model = DataReq
        fields = [
            'task',
            'properties',
            'deadline',
            'done',
        ]
        labels = {
            'task': 'Task',
            'properties': 'Description and links',
            'deadline': 'Deadline',
            'done': 'Done',
        }
        widgets = {
            'task': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm', 'placeholder':
                    'e.g. collect data, select computational tool, create input files, write scripts, adjust model code, update protocol'}
            ),
            'properties': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm', 'placeholder':
                    'e.g. time-period, study sites/geographical domain, resolution, formats, computational routines, detailed protocol. ' +
                    'ENTER LINKS TO DATA & COMPUTATIONAL TOOLS HERE!'}
            ),
            'deadline': DateInput(
                attrs={'class': 'form-control input-sm', 'type': 'date', 'placeholder': 'yyyy-mm-dd'}
            ),
        }

class ExpStepForm(forms.ModelForm):
    class Meta:
        model = ExpStep
        fields = [
            'task',
            'properties',
            'deadline',
            'done',
        ]
        labels = {
            'task': 'Task',
            'properties': 'Output',
            'deadline': 'Deadline',
            'done': 'Done',
        }
        widgets = {
            'task': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm', 'placeholder':
                    'e.g. run models/scripts, visualise results in plots/graphs, compile performance metrics, interpret findings'}
            ),
            'properties': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm', 'placeholder':
                    'preliminary idea of expected results in e.g. maps, graphs, list of findings'}
            ),
            'deadline': DateInput(
                attrs={'class': 'form-control input-sm', 'type': 'date', 'placeholder': 'yyyy-mm-dd'}
            ),
        }

class ReportingForm(forms.ModelForm):
    class Meta:
        model = Reporting
        fields = [
            'task',
            'properties',
            'deadline',
            'done',
        ]
        labels = {
            'task': 'Task',
            'properties': 'Output',
            'deadline': 'Deadline',
            'done': 'Done',
        }
        widgets = {
            'task': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm', 'placeholder':
                    'e.g. write scientific papers, present results at conference, define final Figures and Tables '}
            ),
            'properties': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm', 'placeholder':
                    'e.g. preliminary titles of scientific papers and journals to address, conferences to attend, idea of final Figures and Tables'}
            ),
            'deadline': DateInput(
                attrs={'class': 'form-control input-sm', 'type': 'date', 'placeholder': 'yyyy-mm-dd'}
            ),
        }