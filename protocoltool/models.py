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
    shortTitle = models.CharField(max_length=100)    # a short name for the title
    experimentIdea = models.TextField(blank=True)
    hypothesis = models.TextField(blank=True)
    researchObjective = models.TextField(blank=True)

    dateLastUpdate = models.DateField(blank=True, default=datetime.date.today)
    checked = models.BooleanField(default=False)
    published = models.BooleanField(default=False)

    leadUser = models.ForeignKey(UserProfile, related_name="lead_user", null=True)
    editUsers = models.ManyToManyField(UserProfile, related_name="edit_users")


class Partner(models.Model):
    def __unicode__(self):
        return self.name

    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    organisation = models.CharField(max_length=100)
    lead = models.BooleanField(default=False)
    dataset = models.ForeignKey(BasicDataset)


class DataReq(models.Model):
    task = models.TextField(blank=True)
    taskNr = models.IntegerField(default=1)
    properties = models.TextField(blank=True)
    links = models.TextField(blank=True)
    partner = models.ForeignKey(Partner)
    deadline = models.DateField(blank=True, default=datetime.date.today)
    done = models.BooleanField(default=False)
    dataset = models.ForeignKey(BasicDataset)


class ExpStep(models.Model):
    task = models.TextField(blank=True)
    taskNr = models.IntegerField(default=1)
    properties = models.TextField(blank=True)
    links = models.TextField(blank=True, editable=False)
    partner = models.ForeignKey(Partner)
    deadline = models.DateField(blank=True, default=datetime.date.today)
    done = models.BooleanField(default=False)
    dataset = models.ForeignKey(BasicDataset)


class Reporting(models.Model):
    task = models.TextField(blank=True)
    taskNr = models.IntegerField(default=1)
    properties = models.TextField(blank=True)
    links = models.TextField(blank=True, editable=False)
    partner = models.ForeignKey(Partner)
    deadline = models.DateField(blank=True, default=datetime.date.today)
    done = models.BooleanField(default=False)
    dataset = models.ForeignKey(BasicDataset)


class ExternalProtocol(models.Model):
    shortTitle = models.CharField(max_length=200)
    url = models.URLField(max_length=200)
    dateLastUpdate = models.DateField(blank=True, default=datetime.date.today)