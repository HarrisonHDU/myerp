from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth.views import login, logout
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'erp.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^depot/', include('apps.depot.urls')),
    #(r'^accounts/login/$', 'apps.depot.views.login_view'),
    #(r'^accounts/logout/$', 'apps.depot.views.logout_view'),
    url(r'^sims/', include('apps.sims.urls')),
    url(r'^myerp/', include('apps.myerp.urls')),
)

urlpatterns += staticfiles_urlpatterns()