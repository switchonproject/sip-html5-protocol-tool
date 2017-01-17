from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.conf.urls.static import static
admin.autodiscover()
from django.contrib.auth import views as auth_views
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dme.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # Admin pages
    url(r'^admin/', include(admin.site.urls)),

    # Password reset
    #url(r'^accounts/', include('django.contrib.auth.urls')),
    #url(r'^accounts/password_reset/$', auth_views.password_reset, {'template_name': 'registration/password_reset_form.html'}),
    url(r'^accounts/password_reset/$', auth_views.password_reset, name='password_reset'),
    url(r'^accounts/password_reset/done/$', auth_views.password_reset_done, name='password_reset_done'),
    url(r'^accounts/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',  auth_views.password_reset_confirm, name='password_reset_confirm'),
    url(r'^accounts/reset/done/$', auth_views.password_reset_complete, name='password_reset_complete'),

    # Protocol tool urls
    url(r'^', include('protocoltool.urls', namespace='protocoltool')),
    url(r'^project/', include('protocoltool.urls', namespace='protocoltool')),
)

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
