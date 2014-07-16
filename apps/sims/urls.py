__author__ = 'Administrator'
from django.conf.urls import patterns
from django.contrib.auth.views import login, logout_then_login


urlpatterns = patterns('',
    (r'^$', 'apps.sims.views.index_view'),
    (r'index/$', 'apps.sims.views.index_view'),
    (r'login/$', login, {'template_name': 'sims/login.html'}),
    (r'logout/$', logout_then_login),
    (r'stuinfo/$', 'apps.sims.views.student_info_list'),
    (r'save/$', 'apps.sims.views.save_student'),
    (r'delete/$', 'apps.sims.views.delete_student'),
)
