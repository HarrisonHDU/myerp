__author__ = 'Administrator'
import json
from django.core.serializers import serialize
from django.db.models.query import QuerySet, ValuesQuerySet
from django.db.models import Model
import decimal
import sys
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

