__author__ = 'Administrator'
from django.utils import encoding


def intval(x, default=0):
    '''
    convert str to int value.
    Returns: int
    '''
    if not x or not str(x).isdigit():
        return default
    return int(x)


def start_limit(request, limit_default=0):
    '''
    from HttpRequst get start and limit parameter, POST is first
    Return: start, start+limit
    '''
    start = request.POST.get('start', request.GET.get('start'))
    limit = request.POST.get('limit', request.GET.get('limit'))
    start, limit = intval(start, default=0), intval(limit, default=limit_default)
    return start, start + limit


def callback(msg):
    '''
    return success responseText
    '''
    return {'success': True, 'msg': msg}


def errorcallback(msg='ERROR'):
    '''
    生成 error responseText
    Returns: dict
    '''
    return {'success': False, 'msg': msg}


def curpage(total, data_itmes):
    '''
    为分页store提供数据, {total:XXX, items: XXX}
    Returns: dict
    '''
    return {'total': total, 'items': data_itmes}


def items(value):
    '''
    可以为不需要分页的store提供数据
    Returns: dict
    '''
    return {'items': list(value)}


def getparam(request, *params):
    '''
    获取 *params 指定的参数值, GET first
    Returns: dict
    '''
    kv = dict()
    for p in params:
        if p in request.GET:
            kv[p] = encoding.smart_text(request.GET.get(p), strings_only=True)
        elif p in request.POST:
            kv[p] = encoding.smart_text(request.POST.get(p), strings_only=True)
        else:
            print('parameter {} lost'.format(p))
    return kv