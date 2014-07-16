from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from .models import *
from .tools.tool import Ajax
from .tools import helper
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from erp import settings
from django.contrib.auth.views import logout_then_login
from django.contrib.auth.decorators import login_required

# Create your views here.


@login_required
def index_view(request):
    return render_to_response(
        'sims/index.html',
        locals(),
        context_instance=RequestContext(request)
    )


@Ajax
def student_info_list(request):
    start, limit = helper.start_limit(request, limit_default=5)
    other_params = helper.getparam(request, 'sort', 'dir')
    print(other_params)
    total = Student.objects.count()
    return helper.curpage(total, Student.objects.all()[start:limit])


@Ajax
def save_student(request):
    params = tuple(f.name for f in Student._meta.fields)
    form_params = helper.getparam(request, *params)
    if form_params['id'] == '':
        form_params.pop('id')
    student = Student(**form_params)
    student.save()
    return helper.callback('保存成功')


@Ajax
def delete_student(request):
    params = helper.getparam(request, 'id')
    stid = helper.intval(params['id'])
    Student.objects.get(pk=stid).delete()
    return helper.callback('删除成功')