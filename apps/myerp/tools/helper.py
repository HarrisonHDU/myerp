__author__ = 'Administrator'


def __intval(x, default=0):
    """ convert str to int value. Returns: int """
    if not x or not str(x).isdigit():
        return default
    return int(x)


def __decorator_boolval(fn):
    """ 将形如'true' 或 'false'的字符串装换为 Python中的布尔值,如果不是则返回原值 """
    def wrapper(*args, **kwargs):
        r = fn(*args, **kwargs)
        if isinstance(r, str):
            if r.lower() == 'true':
                return True
            elif r.lower() == 'false':
                return False
        return r

    return wrapper


def __decorator_smart_text(fn):
    def wrapper(*args, **kwargs):
        from django.utils import encoding
        return encoding.smart_text(fn(*args, **kwargs), strings_only=True)

    return wrapper


@__decorator_boolval
@__decorator_smart_text
def __get_param(request, param_name):
    """ 返回指定参数的值,不存在则返回None """
    return request.GET.get(param_name, request.POST.get(param_name, None))


def __get_param_list(request, param_name):
    """ 返回指定参数的值(list)，不存在则返回空列表 """
    return request.GET.getlist(param_name, request.POST.getlist(param_name, []))


def start_limit(request, limit_default=0):
    """ from HttpRequst get start and limit parameter, POST is first。Return: start, start+limit OR None """
    start = request.POST.get('start', request.GET.get('start', None))
    limit = request.POST.get('limit', request.GET.get('limit', None))
    if start is not None and limit is not None:
        start, limit = __intval(start, default=0), __intval(limit, default=limit_default)
        return start, start + limit
    return start, limit


def sort_info(request):
    """ 返回排序参数信息。return: dir, sort, ''|'-'sort OR None """
    sort = request.POST.get('sort', request.GET.get('sort', None))
    dir = request.POST.get('dir', request.GET.get('dir', None))
    if sort is not None and dir is not None:
        return dir, sort, ('-' if dir.upper() == 'DESC' else '') + sort
    return None


def callback(msg):
    """ return success responseText """
    return {'success': True, 'msg': msg}


def errorcallback(msg='ERROR'):
    """ 生成 error responseText。Returns: dict """
    return {'success': False, 'msg': msg}


def curpage(total, data_itmes):
    """ 为分页store提供数据, 返回字典: {total:XXX, items: XXX} """
    return {'total': total, 'items': data_itmes}


def items(value):
    """ 为不需要分页的store提供数据。Returns: dict """
    return {'items': list(value)}


def getparam(request, *params, list_params=[]):
    """ 获取 *params 指定的参数值(GET first).返回: dict(多个参数), object(单个参数), list(单个参数且在list_params中)"""
    if len(params) == 1:
        p = params[0]
        return __get_param_list(request, p) if p in list_params else __get_param(request, p)

    kv = dict()
    for p in params:
        kv[p] = __get_param_list(request, p) if p in list_params else __get_param(request, p)
    return kv