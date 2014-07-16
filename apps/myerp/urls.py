__author__ = 'Administrator'
from django.conf.urls import patterns, url

urlpatterns = patterns('apps.myerp.views',
    url(r'^$', 'index_view'),
    url(r'^sysmenu/$', 'sysmenu_data'),
    url(r'^main/$', 'main_view'),
    url(r'^iframe_tab/$', 'iframe_tab_view'),
    url(r'^sse_data/$', 'sse_view'),
    url(r'^sse/$', 'sse_main_view'),
    url(r'^test/$', 'ajax_test_view', name='ajax_test'),
)

urlpatterns += patterns('apps.myerp.views',
    url(r'^sys/sysmenu/$', 'sysmenu_view'),
    url(r'^sys/productinfo/$', 'product_info_view'),
    url(r'^sys/product_data/$', 'product_data'),
    url(r'^sys/product_node_data/$', 'product_catagory_node_data'),
    url(r'sys/file_output/$', 'file_output'),
    url(r'sys/product_save/$', 'product_save'),
    url(r'sys/product_id_name/$', 'product_id_name', name='sys_product_query'),
)

urlpatterns += patterns('apps.myerp.views',
    url(r'^oc/purchase_order_unsubmit/$', 'purchaseOrder_unsubmit_view', name='oc_pous'),
    url(r'^oc/purchase_order_create/$', 'purchaseOrder_create_view'),
    url(r'^oc/purchase_order_data/$', 'purchaseOrder_data', name='oc_pod'),
    url(r'^oc/purchase_order_detail_data/$', 'purchase_order_detail_data', name='oc_podd'),
)