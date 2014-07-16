__author__ = 'Administrator'
import json
from django.db.models.query import QuerySet, ValuesQuerySet
from django.db.models import Model
import decimal
import datetime
from erp import settings
from django import http


class DjangoJSONEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            return str(o)
        elif isinstance(o, datetime.datetime):
            return o.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(o, datetime.date):
            return o.strftime('%Y-%m-%d')
        elif isinstance(o, datetime.time):
            return o.strftime('%H:%M:%S')
        elif isinstance(o, ValuesQuerySet):
            return list(o)
        elif isinstance(o, QuerySet):
            return list(o)
        elif isinstance(o, Model):
            return {k: getattr(o, k) for k in [f.name for f in o._meta.fields]}
        else:
            return super(DjangoJSONEncoder, self).default(o)


def Ajax(fn):
    def wrapper(*args, **kwargs):
        request = args[0]
        if not settings.DEBUG and not request.is_ajax():
            raise http.Http404
        result = fn(*args, **kwargs)
        result = json.dumps(result, cls=DjangoJSONEncoder)
        return http.HttpResponse(result, content_type="application/json")

    return wrapper


def analysis_iterable_object(iterable_obj, rulers, item_type='dict'):
    """
    根据d中定义的解析规则解析可迭代对象iterable_obj，返回包含解析结果的list对象,
    参数item_type = 'dict'适用于JSON类型数据，item_type = 'list' 适用于Array类型数据
    参数d是一个元组,元组中的每一项都是一个二元元组，定义解析规则，例如：
    (
        ('id', 'id'),
        ('name', '__CONST__Kobe'),
        ('related_obj_name', lambda obj: getattr(getattr(obj, 'related_id'),'related_name')),
        ('is_delete', True),
    )
    上面例子中的解析规则如下：
        id 表示可迭代对象中每一项的属性id
        name 表示常量 'Kone'
        related_obj_name 表示调用lambda表达式(可调用对象)获得相应的值
        is_delete 表示为常量 True
    """
    def add_item(o, kname, el):
        if isinstance(o, dict):
            o[kname] = el
        elif isinstance(o, list):
            o.append(el)

    const_strip_length = len('__CONST__')
    r = list()
    for item in iterable_obj:
        element = dict() if item_type == 'dict' else list()
        for ruler in rulers:
            # 每一个规则元组都可以看作是一个键值对
            k, v = ruler
            if callable(v):
                # 可调用对象
                add_item(element, k, v(item))
            elif not isinstance(v, str):
                # 整形，布尔型等非字符串对象
                add_item(element, k, v)
            elif v.startswith('__CONST__'):
                # 字符串常量
                add_item(element, k, v[const_strip_length:])
            else:
                # 对象属性
                add_item(element, k, getattr(item, v))
        r.append(element)
    return r