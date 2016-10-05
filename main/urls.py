from django.conf import settings
from django.conf.urls import patterns, url, include
from django.contrib import admin
from django.conf.urls.static import static
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'dme.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('protocoltool.urls', namespace='protocoltool')),
    url(r'^project/', include('protocoltool.urls', namespace='protocoltool')),
)

# if settings.DEBUG:
#     urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
