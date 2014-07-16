from django.contrib import admin
from apps.workflow.models import *

# Register your models here.


class WFNode01Admin(admin.ModelAdmin):
    list_display = ('node_id', 'node_name', 'node_type')


class WF01Admin(admin.ModelAdmin):
    list_display = ('path_id', 'south', 'dist', 'condition', 'auto')


class WFTrace01Admin(admin.ModelAdmin):
    list_display = ('instance_id', 'path_id', 'executor', 'execute_datetime', 'comment')


class WFState01Admin(admin.ModelAdmin):
    list_display = ('instance_id', 'node_id')


admin.site.register(WFNode01, WFNode01Admin)
admin.site.register(WF01, WF01Admin)
admin.site.register(WFTrace01, WFTrace01Admin)
admin.site.register(WFState01, WFState01Admin)