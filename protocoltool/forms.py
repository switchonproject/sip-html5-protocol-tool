from django import forms
from .models import BasicDataset, Partner, Publication, DataReq, ExpStep, Reporting, UserProfile
from django.forms.widgets import DateInput, Textarea, TextInput, EmailInput, PasswordInput
from django.contrib.auth.models import User


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        labels = {
            'username': 'Username',
            'email': 'Email',
            'password': 'Password',
        }
        widgets = {
            'username': TextInput(
                attrs={'class': 'form-control input-sm', 'autofocus': 'autofocus', 'placeholder': 'your preferred login (no spaces)'}
            ),
            'email': EmailInput(
                attrs={'class': 'form-control input-sm', 'autofocus': 'autofocus', 'placeholder': 'your email'}
            ),
            'password': PasswordInput(
                attrs={'class': 'form-control input-sm', 'autofocus': 'autofocus'}
            )
        }


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['organisation']
        labels = {'organisation' : 'Organisation'}
        widgets = {
            'organisation': TextInput(
                attrs={'class': 'form-control input-sm', 'autofocus': 'autofocus'}
            )
        }



class BasicDatasetForm(forms.ModelForm):
    class Meta:
        model = BasicDataset
        fields = [
            'title',
            'shortTitle',
            'experimentIdea',
            'hypothesis',
            'researchObjective',
        ]
        labels = {
            'title': 'Full name',
            'shortTitle': 'Short name',
            'experimentIdea': 'Experiment Idea',
            'hypothesis' : 'Hypothesis',
            'researchObjective': 'Research Objective',
        }
        widgets = {
            'title': TextInput(
                attrs={'class': 'form-control input-sm', 'autofocus': 'autofocus'}
            ),
            'shortTitle': TextInput(
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


class PublicationForm(forms.ModelForm):
    class Meta:
        model = Publication
        fields = [
            'name',
            'type',
        ]
        labels = {
            'name': 'Paper Title',
            'type': 'DOI',
        }
        widgets = {
            'name': Textarea(
                attrs={'rows':3, 'style':'resize:vertical;', 'class': 'form-control input-sm', 'autofocus': 'autofocus', 'placeholder': 'Please use the following format for publication references: Authors list (Date): Title of publication, Journal, Volume, Pages'}
            ),
            'type': TextInput(
                attrs={'class': 'form-control input-sm', 'autofocus': 'autofocus', 'placeholder': 'the DOI or link to published paper'}
            ),
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
            'links',
            'deadline',
            'done',
        ]
        labels = {
            'task': 'Task',
            'properties': 'Description',
            'links': 'Links',
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
                    'e.g. time-period, study sites/geographical domain, resolution, formats, computational routines, detailed protocol. '}
            ),
            'links': TextInput(
                attrs={'class': 'form-control input-sm', 'autofocus': 'autofocus', 'placeholder': 'e.g urls associated'}
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
            'links',
            'deadline',
            'done',
        ]
        labels = {
            'task': 'Task',
            'properties': 'Description',
            'links': 'Links',
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
            'links': TextInput(
                attrs={'class': 'form-control input-sm', 'autofocus': 'autofocus', 'placeholder': 'e.g urls associated'}
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
            'links',
            'deadline',
            'done',
        ]
        labels = {
            'task': 'Task',
            'properties': 'Description',
            'links': 'Links',
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
            'links': TextInput(
                attrs={'class': 'form-control input-sm', 'autofocus': 'autofocus', 'placeholder': 'e.g urls associated'}
            ),
            'deadline': DateInput(
                attrs={'class': 'form-control input-sm', 'type': 'date', 'placeholder': 'yyyy-mm-dd'}
            ),
        }