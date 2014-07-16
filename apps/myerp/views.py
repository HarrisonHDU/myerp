from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from apps.myerp.tools.tool import Ajax, analysis_iterable_object
from apps.myerp.tools import helper
from apps.myerp.models import SysMenu, Product, ProductCategoryPrimary, ProductCategorySecondary, \
    PurchaseOrder, PurchaseOrderDetail
from apps.myerp.tools.dataDocumented import DOC_Handler
from erp.settings import DATA_DOCUMENTED_SETTINGS
from django.http import HttpResponse
import datetime
from apps.myerp.settings import SYSMENU_EXPAND
from apps.myerp.customExceptions import RequiredParamsLost, ParamsInvalid

# Create your views here.


def index_view(request):
    return render_to_response(
        'myerp/index.html',
        locals(),
        context_instance=RequestContext(request)
    )


def main_view(request):
    return render_to_response(
        'myerp/main.html',
        locals(),
        context_instance=RequestContext(request)
    )


def iframe_tab_view(request):
    return render_to_response(
        'myerp/iframe_tab.html',
        locals(),
        context_instance=RequestContext(request)
    )


def ajax_test_view(request):
    return render_to_response(
        'myerp/test.html',
        locals(),
        context_instance=RequestContext(request)
    )

@Ajax
def sysmenu_data(request):
    """
    系统菜单信息
    """
    def add_node(node, all_nodes):
        #assert isinstance(node, SysMenu)
        if node.menu_is_catalogue is not True:
            return {
                'id': node.menu_id,
                'text': node.menu_name,
                'leaf': True,
                'href': reverse(node.menu_action) if node.menu_action != '' else '',
                # 为hrefTarget 设置默认值，前端会在单击节点事件时替换为合适的iframe name或者由自定义监听函数处理
                'hrefTarget': '_blank'
            }
        else:
            return {
                'id': node.menu_id,
                'text': node.menu_name,
                'href': reverse(node.menu_action) if node.menu_action != '' else '',
                'expanded': SYSMENU_EXPAND,
                'children': [add_node(n, all_nodes) for n in all_nodes.filter(menu_father_id__exact=node.menu_id)]
            }

    root_id = SysMenu.root_menu_id()
    all_child_item = SysMenu.objects.exclude(menu_id__exact=root_id).order_by('menu_order_no')
    node_list = []
    for menu_item in all_child_item.filter(menu_father_id__exact=root_id):
        node_list.append(add_node(menu_item, all_child_item))
    return node_list


def sysmenu_view(request):
    return render_to_response(
        'myerp/sys/sysmenu.html',
        locals(),
        context_instance=RequestContext(request)
    )


def product_info_view(request):
    return render_to_response(
        'myerp/sys/productInfo.html',
        {
            'DATA_DOCUMENTED_SETTINGS': DATA_DOCUMENTED_SETTINGS
        },
        context_instance=RequestContext(request)
    )


@Ajax
def product_data(request):
    """
    返回产品基础信息数据
    """
    start, limit = helper.start_limit(request)
    other_params = helper.getparam(request, 'sort', 'dir')
    total = Product.objects.count()
    if 'sort' in other_params and 'dir' in other_params:
        direction = '-' if other_params['dir'] == 'DESC' else ''
        result = Product.objects.order_by(direction + other_params['sort'])
    else:
        result = Product.objects.all()
    data = analysis_iterable_object(result[start:limit], (
        ('id', 'id'),
        ('pid', 'pid'),
        ('sec_id', lambda obj: getattr(getattr(obj, 'sec_id'), 'pcid')),
        ('sec_name', lambda obj: getattr(getattr(obj, 'sec_id'), 'name')),
        ('name', 'name'),
        ('create_date', 'create_date'),
        ('purchase_price', 'purchase_price'),
        ('sell_price', 'sell_price'),
        ('warning_amount_bottom', 'warning_amount_bottom'),
        ('warning_amount_top', 'warning_amount_top'),
        ('is_warning_active', 'is_warning_active'),
        ('remark', 'remark'),
        ('is_delete', 'is_delete'),
    ))
    return helper.curpage(total, data)


@Ajax
def product_id_name(request):
    """
    返回产品编码-名称
    参数:
        data_type: [json|array]
        search_type: [name|id]
        query: [xxx|]
        start: [xxx|]
        limit: [xxx|]
    返回: Array(id,name) | Json{items:[XXX][,total:xxx]}
    """
    params = helper.getparam(request, 'data_type', 'search_type', 'query')
    start, limit = helper.start_limit(request)

    r = Product.objects.all()
    if params['query'] is not None:
        if params['search_type'].lower() == 'name':
            r = r.filter(name__contains=params['query'])
        elif params['search_type'].lower() == 'id':
            r = r.filter(pid__contains=params['query'])
        else:
            raise ParamsInvalid("search_type必须是name或id")

    # 默认返回类型是JSON
    if params['data_type'] is None: params['data_type'] = 'json'

    if params['data_type'].lower() == 'json':
        r = analysis_iterable_object(r, (('pid', 'pid'), ('name', 'name')))
        if start is not None and limit is not None:
            total = len(r)
            r = r[start:limit]
            return helper.curpage(total, r)
        return helper.items(r)
    elif params['data_type'].lower() == 'array':
        return analysis_iterable_object(r, (('pid', 'pid'), ('name', 'name')), item_type='list')
    else:
        raise ParamsInvalid("data_type 必须是json或array")



@Ajax
def product_catagory_node_data(request):
    """
    返回产品种类异步树节点数据
    """
    node_id = helper.getparam(request, 'node')
    if node_id == '0':
        # 返回一级种类科目, 即使一级科目没有父节点也要返回father=''，这样前台填充表单时，可以设置下拉框为空
        return analysis_iterable_object(ProductCategoryPrimary.objects.all(), (
            ('id', 'pcid'),
            ('name', 'name'),
            ('remark', 'remark'),
            ('is_delete', 'is_delete'),
            ('father', '__CONST__'),
        ))
    else:
        # 返回二级种类科目(在本项目中，项目种类只有二级，所以这一级就是叶子节点)
        r = ProductCategorySecondary.objects.filter(pcpid__exact=node_id)
        return analysis_iterable_object(r, (
            ('id', 'pcid'),
            ('father', '__CONST__' + node_id),
            ('name', 'name'),
            ('remark', 'remark'),
            ('is_delete', 'is_delete'),
            ('leaf', True),
        ))


@Ajax
def file_output(request):
    """导出信息到文件,参数output_type指定信息种类"""
    output_type = helper.getparam(request, 'output_type')['output_type']
    # 下面这行代码是一个安全漏洞，这里是利用eval函数的表达式求值得到数组形式的字符串中的数组，
    # 如果未来有更好的解析方法，应该尽快替换。eval是邪恶的！
    output_type = eval(output_type, {"__builtins__": None}, {})
    for t in output_type:
        DOC_Handler[t]()
    return helper.callback('产品种类数据文件化成功!')


def sse_view(request):
    response = HttpResponse(
        content="data: {}\n\n".format(datetime.datetime.today()),
        content_type="text/event-stream"
    )
    response["Cache-Control"] = "no-cache"
    return response


def sse_main_view(request):
    return render_to_response(
        'myerp/sse_test.html',
        context_instance=RequestContext(request)
    )


@Ajax
def product_save(request):
    """[更新/新建]产品"""
    is_update = True
    params = list(f.name for f in Product._meta.fields)
    # 不需要更新创建日期
    params.remove('create_date')
    form_params = helper.getparam(request, *params)
    sec_id = int(form_params.pop('sec_id'))
    if form_params['id'] == '':
        form_params.pop('id')
        is_update = False
    product = Product(sec_id=ProductCategorySecondary.objects.get(pcid__exact=sec_id), **form_params)
    # 因为在更新时PCreateDate是不需要更新的，save方法必须手动指定要更新的字段。
    # 所以这里不得不区分insert和update
    if is_update:
        params.remove('id')
        product.save(update_fields=params)
    else:
        product.save()
    return helper.callback("保存成功")


def purchaseOrder_unsubmit_view(request):
    return render_to_response(
        'myerp/oc/purchaseOrder_unsubmit.html',
        {'next': reverse(purchaseOrder_create_view)},
        context_instance=RequestContext(request)
    )


def purchaseOrder_create_view(request):
    """[新建/编辑]采购订单"""
    order_id = helper.getparam(request, 'order_id')
    back = reverse(purchaseOrder_unsubmit_view)
    if order_id is not None:
        # 返回采购订单数据
        purchase_order = PurchaseOrder.objects.get(pid__exact=order_id)
        purchase_order_detail = purchase_order.purchaseorderdetail_set

    return render_to_response(
        'myerp/oc/purchaseOrder_create.html',
        locals(),
        context_instance=RequestContext(request)
    )


@Ajax
def purchaseOrder_data(request):
    """采购订单主订单数据"""
    sort_info = helper.sort_info(request)
    start, limit = helper.start_limit(request)
    total = PurchaseOrder.objects.count()
    if sort_info is None:
        r = PurchaseOrder.objects.all()
    else:
        r = PurchaseOrder.objects.order_by(sort_info[2])
    r = analysis_iterable_object(r[start:limit], (
        ('id', 'id'),
        ('pid', 'pid'),
        ('total', 'total'),
        ('creater', lambda obj: getattr(getattr(getattr(obj, 'creater'), 'user'), 'username')),
        ('creater_eid', lambda obj: getattr(getattr(obj, 'creater'), 'eid')),
        ('create_datetime', 'create_datetime'),
        ('last_modifier', lambda obj: getattr(getattr(getattr(obj, 'last_modifier'), 'user'), 'username')),
        ('last_modifier_eid', lambda obj: getattr(getattr(obj, 'last_modifier'), 'eid')),
        ('last_modify_datetime', 'last_modify_datetime'),
    ))
    return helper.curpage(total, r)


@Ajax
def purchase_order_detail_data(request):
    """采购订单明细数据"""
    sort_info = helper.sort_info(request)
    order_id = helper.getparam(request, 'order_id')
    r = PurchaseOrder.objects.get(pid__exact=order_id).purchaseorderdetail_set.all()
    if sort_info is not None:
        r = r.order_by(sort_info[2])
    r = analysis_iterable_object(r, item_type='list', rulers=(
        ('id', 'id'),
        ('product_id', 'product_id'),
        ('product_name', lambda obj: getattr(getattr(obj, 'product_id'), 'name')),
        ('unit_price', 'unit_price'),
        ('amount', 'amount'),
    ))
    return r