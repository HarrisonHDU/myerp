from django.conf.urls import patterns
from .models import *
from .views import *

urlpatterns = patterns('',
    (r'product/create/$', create_product),
    (r'product/list/$', list_product),
    (r'product/edit/(?P<id>[^/]+)/$', edit_product),
    (r'product/view/(?P<id>[^/]+)/$', view_product),
    (r'store/$', store_view),
    (r'cart/view/$', view_cart),
    (r'cart/add/(?P<product_id>[\d+])/$', add_to_cart),
    (r'cart/clear/$', clear_cart),
)
