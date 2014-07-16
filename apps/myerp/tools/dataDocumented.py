__author__ = 'Harrison'
from apps.myerp.models import ProductCategoryPrimary, ProductCategorySecondary
from apps.myerp.tools.tool import DjangoJSONEncoder, analysis_iterable_object
from erp.settings import DATA_DOCUMENTED_SETTINGS
import os
import json

#数据文件化处理器
DOC_Handler = dict()


def handler_register(hander_name, handler):
    """
    数据文件化处理器注册函数
    """
    DOC_Handler[hander_name] = handler


def data_doc_file_path(ftype):
    return os.path.join(DATA_DOCUMENTED_SETTINGS['BASE_DIR'], DATA_DOCUMENTED_SETTINGS[ftype])


def product_catagory_primary():
    """
    一级产品信息数据文件化
    格式: 普通JSON数组
    """
    file_path = data_doc_file_path('product_catagory_primary_file_name')
    with open(file_path, mode='w', encoding='utf-8') as f:
        json.dump({'items': ProductCategoryPrimary.objects.all()}, fp=f, cls=DjangoJSONEncoder)


def product_catagory():
    """
    产品种类数据文件化
    格式: 适用于tree的JSON数组
    """
    file_path = data_doc_file_path('product_catagory_file_name')
    with open(file_path, mode='w', encoding='utf-8') as f:
        primary_objs = analysis_iterable_object(
            ProductCategoryPrimary.objects.filter(is_delete__exact=False), {
                'id': 'pcid',
                'text': 'name',
                'children': []
            }
        )
        for item in primary_objs:
            secondary_objs = analysis_iterable_object(
                ProductCategorySecondary.objects.filter(is_delete__exact=False, pcpid__pcid__exact=item['id']), {
                    'id': 'pcid',
                    'text': 'name',
                    'leaf': True
                }
            )
            item['children'] = secondary_objs
        json.dump(primary_objs, fp=f, cls=DjangoJSONEncoder)


# 注册一级产品信息数据文件化处理函数
handler_register('product_catagory_primary', product_catagory_primary)
# 注册产品种类数据文件化处理函数
handler_register('product_catagory', product_catagory)