# Create your views here.

from django import forms
from django.template import RequestContext
from django.http import HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.core.paginator import Paginator
from django.core.urlresolvers import reverse
import datetime
from django.shortcuts import render_to_response
from django.core import serializers
import json
import decimal
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# app specific files

from .models import *
from .forms import *


def to_json(python_object):
    if isinstance(python_object, Cart):
        return {
            '__class__': 'Cart',
            '__value__': {
                'items': serializers.serialize('json', python_object.items),
                'total_price': str(python_object.total_price)
            }
        }
    raise TypeError(repr(python_object) + ' is not JSON serializable')


def from_json(json_object):
    if '__class__' in json_object:
        if json_object['__class__'] == 'Cart':
            return Cart(items=[deserialized_object.object for deserialized_object in serializers.deserialize('json', json_object['__value__']['items'])],
                        total=decimal.Decimal(json_object['__value__']['total_price']))
    return json_object


def create_product(request):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        form = ProductForm()
    t = get_template('depot/create_product.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


@login_required
def list_product(request):
    list_items = Product.objects.all()
    paginator = Paginator(list_items, 10)

    try:
        page = int(request.GET.get('page', '1'))
    except ValueError:
        page = 1

    try:
        list_items = paginator.page(page)
    except:
        list_items = paginator.page(paginator.num_pages)

    t = get_template('depot/p_list_product.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def view_product(request, id):
    product_instance = Product.objects.get(id=id)

    t = get_template('depot/view_product.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def edit_product(request, id):
    product_instance = Product.objects.get(id=id)

    form = ProductForm(request.POST or None, instance=product_instance)

    if form.is_valid():
        form.save()

    t = get_template('depot/edit_product.html')
    c = RequestContext(request, locals())
    return HttpResponse(t.render(c))


def store_view(request):
    products = Product.objects.filter(date_available__lt=datetime.datetime.now().date()).order_by('-date_available')
    number = len(products)
    try:
        cart = json.loads(request.session.get('cart', None), object_hook=from_json)
    except:
        cart = Cart()
    return render_to_response(
        template_name='depot/store.html',
        dictionary=locals(),
        context_instance=RequestContext(request)
    )


def view_cart(request):
    try:
        cart = json.loads(request.session.get("cart", None), object_hook=from_json)
    except:
        cart = None
    if not cart:
        cart = Cart()
        request.session['cart'] = json.dumps(cart, default=to_json)
    return render_to_response('depot/view_cart.html', locals(), context_instance=RequestContext(request))


def add_to_cart(request, product_id):
    product = Product.objects.get(id=product_id)
    try:
        cart = json.loads(request.session['cart'], object_hook=from_json)
    except:
        cart = None
    if not cart:
        cart = Cart()
        request.session['cart'] = json.dumps(cart, default=to_json)
    cart.add_product(product)
    request.session['cart'] = json.dumps(cart, default=to_json)
    return view_cart(request)


def clear_cart(request):
    request.session['cart'] = json.dumps(Cart(), default=to_json)
    return view_cart(request)


def login_view(request):
    user = authenticate(username=request.POST.get('username', None),
                        password=request.POST.get('password', None))
    if user is not None:
        login(request, user)
        print(request.user)
        return list_product(request)
    else:
        # 验证失败，暂不处理
        return store_view(request)


def logout_view(request):
    logout(request)
    return store_view(request)

