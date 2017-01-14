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

    # User authorization and password reset
    url(r'^accounts/', include('django.contrib.auth.urls')),

    # Protocol tool urls
    url(r'^', include('protocoltool.urls', namespace='protocoltool')),
    url(r'^project/', include('protocoltool.urls', namespace='protocoltool')),
)

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
