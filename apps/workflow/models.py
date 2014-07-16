from django.db import models
from apps.myerp.models import PurchaseOrder, Employee
# Create your models here.

RELATED_NAME_PREFIX = '%(app_label)s_%(class)s_'


class WFNode01(models.Model):
    """01流程节点表"""
    START, NORMAL, END, OTHER = 's', 'n', 'e', 'o'
    node_type_enum = (
        (START, 'start'),
        (NORMAL, 'normal'),
        (END, 'end'),
        (OTHER, 'other')
    )

    node_id = models.PositiveSmallIntegerField(null=False, unique=True, db_column='NodeID')
    node_name = models.CharField(max_length=30, null=False, blank=True, db_column='NodeName')
    node_type = models.CharField(max_length=10, null=False, choices=node_type_enum, default=NORMAL,
                                 db_column='NodeType')


class WF01(models.Model):
    """01流程状态迁移表"""
    path_id = models.PositiveSmallIntegerField(null=False, unique=True, db_column='PathID')
    south = models.ForeignKey(to=WFNode01, to_field='node_id', on_delete=models.CASCADE, db_column='South',
                              related_name=RELATED_NAME_PREFIX+'south')
    dist = models.ForeignKey(to=WFNode01, to_field='node_id', on_delete=models.CASCADE, db_column='Dist',
                             related_name=RELATED_NAME_PREFIX+'dist')
    condition = models.CharField(max_length=255, null=False, blank=True, db_column='Condition',
                                 help_text="状态迁移条件，若条件变量为整形{var}；若条件变量为字符串'{var}'。语法格式同SQL")
    auto = models.BooleanField(null=False, default=False, db_column='Auto')


class WFTrace01(models.Model):
    """01流程轨迹表"""
    instance_id = models.ForeignKey(to=PurchaseOrder, to_field='pid', on_delete=models.CASCADE,
                                    db_column='InstanceID', help_text='流程实例ID')
    path_id = models.ForeignKey(to=WF01, to_field='path_id', on_delete=models.CASCADE, db_column='PathID')
    executor = models.ForeignKey(to=Employee, to_field='eid', null=True, on_delete=models.SET_NULL,
                                 db_column='Executor', help_text="执行人，‘000’为自动执行")
    execute_datetime = models.DateTimeField(null=False, auto_now_add=True, db_column='ExecuteDateTime')
    comment = models.CharField(max_length=255, null=False, blank=True, db_column='Comment')


class WFState01(models.Model):
    """01流程状态信息表"""
    instance_id = models.ForeignKey(to=PurchaseOrder, to_field='pid', on_delete=models.CASCADE,
                                    db_column='InstanceID', help_text='流程实例ID')
    node_id = models.ForeignKey(to=WFNode01, to_field='node_id', db_column='NodeID',
                                on_delete=models.CASCADE, help_text='流程实例当前所处节点')