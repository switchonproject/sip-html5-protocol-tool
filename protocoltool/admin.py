from django.contrib import admin
from .models import BasicDataset, Partner, DataReq, ExpStep, Reporting, ExternalProtocol, UserProfile

# Register your models here.
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'organisation')

class BasicDatasetAdmin(admin.ModelAdmin):
    list_display = ('id',
            'title',
            'shortTitle',
            'leadUser',
            'published',
            'hidden')

class PartnerAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'email', 'organisation', 'lead')

class DataReqAdmin(admin.ModelAdmin):
    list_display = ('task', 'taskNr', 'properties', 'links', 'partner', 'deadline', 'done')

class ExpStepAdmin(admin.ModelAdmin):
    list_display = ('task', 'taskNr', 'properties', 'links', 'partner', 'deadline', 'done')

class ReportingAdmin(admin.ModelAdmin):
    list_display = ('task', 'taskNr', 'properties', 'links', 'partner', 'deadline', 'done')

class ExternalProtocolAdmin(admin.ModelAdmin):
    list_display = ('shortTitle', 'url', 'dateLastUpdate')

admin.site.register(UserProfile, UserProfileAdmin)
admin.site.register(BasicDataset, BasicDatasetAdmin)
admin.site.register(Partner, PartnerAdmin)
admin.site.register(DataReq, DataReqAdmin)
admin.site.register(ExpStep, ExpStepAdmin)
admin.site.register(Reporting, ReportingAdmin)
admin.site.register(ExternalProtocol, ExternalProtocolAdmin)