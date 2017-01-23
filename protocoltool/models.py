from django.db import models
from django.contrib.auth.models import User
import datetime


class UserProfile(models.Model):
    # Link UserProfile to a User model instance.
    user = models.OneToOneField(User)

    # The additional attributes we wish to include
    organisation = models.CharField(max_length=100)

    # Override the __unicode__() method to return out something meaningful
    def __unicode__(self):
        return self.user.username


class BasicDataset(models.Model):
    def __unicode__(self):
        return self.title

    title = models.CharField(max_length=200)
    shortTitle = models.CharField(max_length=60)  # a short name for the title
    experimentIdea = models.TextField(blank=True, max_length=1200)
    hypothesis = models.TextField(blank=True, max_length=600)
    researchObjective = models.TextField(blank=True, max_length=130)
    dateLastUpdate = models.DateField(blank=True, default=datetime.date.today)
    hidden = models.BooleanField(default=True)
    published = models.BooleanField(default=False)
    # Foreing Keys
    leadUser = models.ForeignKey(UserProfile, related_name="lead_user", null=True)
    editUsers = models.ManyToManyField(UserProfile, related_name="edit_users")

class Publication(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=100)
    type = models.CharField(max_length=100)

    # Foreing Keys
    dataset = models.ForeignKey(BasicDataset)

class Partner(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    organisation = models.CharField(max_length=100)
    lead = models.BooleanField(default=False)
    # Foreing Keys
    dataset = models.ForeignKey(BasicDataset)

class DataReq(models.Model):
    task = models.TextField(blank=True)
    taskNr = models.IntegerField(default=1)
    properties = models.TextField(blank=True)
    links = models.TextField(blank=True)
    partner = models.ForeignKey(Partner)
    deadline = models.DateField(blank=True, default=datetime.date.today)
    done = models.BooleanField(default=False)
    # Foreing Keys
    dataset = models.ForeignKey(BasicDataset)

class ExpStep(models.Model):
    task = models.TextField(blank=True)
    taskNr = models.IntegerField(default=1)
    properties = models.TextField(blank=True)
    links = models.TextField(blank=True, editable=False)
    partner = models.ForeignKey(Partner)
    deadline = models.DateField(blank=True, default=datetime.date.today)
    done = models.BooleanField(default=False)
    # Foreing Keys
    dataset = models.ForeignKey(BasicDataset)

class Reporting(models.Model):
    task = models.TextField(blank=True)
    taskNr = models.IntegerField(default=1)
    deadline = models.DateField(blank=True, default=datetime.date.today)
    done = models.BooleanField(default=False)
    properties = models.TextField(blank=True)
    links = models.TextField(blank=True, editable=False)
    # Foreing Keys
    partner = models.ForeignKey(Partner)
    dataset = models.ForeignKey(BasicDataset)

class ExternalProtocol(models.Model):
    shortTitle = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    dateLastUpdate = models.DateField(blank=True, default=datetime.date.today)