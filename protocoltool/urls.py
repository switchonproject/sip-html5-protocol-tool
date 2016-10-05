from django.conf.urls import patterns, url

from protocoltool import views

urlpatterns = patterns('',

    #url(r'^form/$', views.formBasic, name='formbasic'),

    url(r'^register/$', views.register, name='register'),
    url(r'^login/$', views.user_login, name='login'),
    url(r'^logout/$', views.user_logout, name='logout'),

    url(r'^$', views.review, name='protocoloverview_review'),
    url(r'^participate/$', views.participate, name='protocoloverview_participate'),
    url(r'^review/$', views.review, name='protocoloverview_review'),

    url(r'^overviewaction/$', views.protocolOverviewAction, name='protocoloverview_action'),

    url(r'^createprotocol/$', views.createProtocol, name='createprotocol'),
    url(r'^form/(?P<dataset_id>\d*)/$', views.formAll, name='formall'),
    url(r'^view/(?P<dataset_id>\d*)/$', views.viewProtocol, name='viewprotocol'),

    url(r'^saveexperimentinfo/$', views.saveExperimentInfo, name='save_experiment_info'),

    url(r'^addpartner/$', views.addPartner, name='add_partner'),
    url(r'^updatepartner/$', views.updatePartner, name='update_partner'),
    url(r'^deletepartner/$', views.deletePartner, name='delete_partner'),
                       
    url(r'^addreq/$', views.addReq, name='add_req'),
    url(r'^updatereq/$', views.updateReq, name='update_req'),
    url(r'^deletereq/$', views.deleteReq, name='delete_req'),
    url(r'^increasereq/$', views.increaseReq, name='increase_req'),
    url(r'^decreasereq/$', views.decreaseReq, name='decrease_req'),

    url(r'^addstep/$', views.addExpStep, name='add_step'),
    url(r'^updatestep/$', views.updateExpStep, name='update_step'),
    url(r'^deletestep/$', views.deleteExpStep, name='delete_step'),
    url(r'^increaseexpstep/$', views.increaseExpStep, name='increase_expstep'),
    url(r'^decreaseexpstep/$', views.decreaseExpStep, name='decrease_expstep'),

    url(r'^addreporting/$', views.addReporting, name='add_reporting'),
    url(r'^updatereporting/$', views.updateReporting, name='update_reporting'),
    url(r'^deletereporting/$', views.deleteReporting, name='delete_reporting'),
    url(r'^increasereporting/$', views.increaseReporting, name='increase_reporting'),
    url(r'^decreasereporting/$', views.decreaseReporting, name='decrease_reporting'),
)