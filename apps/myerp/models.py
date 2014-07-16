from django.db import models
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save

# Create your models here.
# 需要说明的几个问题:
# 1> Django模型没有提供 on_update 的字段选项，此类的约束的定义只能做在数据库定义中


class BaseModel(models.Model):
    """基础表"""
    remark = models.CharField(null=False, blank=True, max_length=255, db_column='Remark', help_text='备注')
    is_delete = models.BooleanField(null=False, default=False, db_column='IsDelete')

    class Meta:
        abstract = True


class Product(BaseModel):
    """产品基础信息表"""
    pid = models.PositiveIntegerField(null=False, unique=True, db_column='PID',
                                      verbose_name='产品ID', help_text='产品ID')
    sec_id = models.ForeignKey(to='ProductCategorySecondary', to_field='pcid', null=True,
                               on_delete=models.SET_NULL, db_column='PSecID', help_text='产品二级种类ID')
    name = models.CharField(max_length=50, null=False, default='', blank=True,
                            help_text='产品名称', db_column='PName')
    create_date = models.DateTimeField(null=False, auto_now_add=True, db_column='PCreateDate',
                                       help_text='创建时间')
    purchase_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False,
                                         db_column='PurchasePrice', help_text='参考进价')
    sell_price = models.DecimalField(max_digits=10, decimal_places=2, default=0, null=False,
                                     db_column='SellPrice', help_text='参考售价')
    warning_amount_bottom = models.PositiveIntegerField(null=False, default=0, db_column='WarningAmountBottom',
                                                        help_text='库存预警下限')
    warning_amount_top = models.PositiveIntegerField(null=False, default=0, db_column='WarningAmountTop',
                                                     help_text='库存预警上限')
    is_warning_active = models.BooleanField(null=False, default=False, db_column='IsWarningActive',
                                            help_text='是否启用库存预警')

    def __str__(self):
        return self.name


class ProductCategoryPrimary(BaseModel):
    """一级产品种类表"""
    pcid = models.PositiveIntegerField(null=False, unique=True, db_column='PCID', help_text='一级种类ID')
    name = models.CharField(null=False, blank=True, max_length=45, db_column='PCNAME', help_text='种类名称')

    def __str__(self):
        return self.name


class ProductCategorySecondary(BaseModel):
    """二级产品种类表"""
    pcid = models.PositiveIntegerField(null=False, unique=True, db_column='PCID', help_text='二级种类ID')
    pcpid = models.ForeignKey(to=ProductCategoryPrimary, to_field='pcid', db_column='PCPID',
                              on_delete=models.CASCADE)
    name = models.CharField(null=False, blank=True, max_length=45, db_column='PCNAME', help_text='种类名称')

    def __str__(self):
        return self.name


class Employee(models.Model):
    """员工表"""
    MALE, FEMALE = 'm', 'f'
    sex_enum = ((MALE, 'Male'), (FEMALE, 'Female'))

    user = models.OneToOneField(to=User)
    eid = models.CharField(max_length=10, null=False, unique=True, db_column='EID')
    sex = models.CharField(max_length=1, choices=sex_enum, default=MALE, db_column='ESex')

    def __str__(self):
        return "{}({})".format(self.user.username, self.eid)


class PurchaseOrder(BaseModel):
    """采购订单表"""
    pid = models.BigIntegerField(null=False, unique=True, db_column='PID')
    create_datetime = models.DateTimeField(null=False, auto_now_add=True, db_column='PDateTime', help_text='创建时间')
    creater = models.ForeignKey(to=Employee, to_field='eid', on_delete=models.SET_NULL, null=True,
                                db_column='PCreater', related_name='%(app_label)s_%(class)s_creater')
    total = models.DecimalField(null=False, max_digits=10, decimal_places=2, default=0, db_column='PTotal',
                                help_text='订单总金额')
    last_modifier = models.ForeignKey(to=Employee, to_field='eid', on_delete=models.SET_NULL,
                                      db_column='PLastModifier', null=True,
                                      related_name='%(app_label)s_%(class)s_last_modifier')
    last_modify_datetime = models.DateTimeField(auto_now=True, db_column='PLastModifyDateTime')


class PurchaseOrderDetail(BaseModel):
    """采购订单明细表"""
    poid = models.ForeignKey(to=PurchaseOrder, to_field='pid', on_delete=models.CASCADE,
                             db_column='POID', help_text='主表PID')
    product_id = models.ForeignKey(to=Product, to_field='pid', on_delete=models.SET_NULL, null=True)
    unit_price = models.DecimalField(null=False, max_digits=8, decimal_places=2, default=0,
                                     db_column='PODUnitPrice', help_text='采购单价')
    amount = models.PositiveIntegerField(null=False, default=0, db_column='PODAmount')


class SysMenu(BaseModel):
    """系统菜单"""
    menu_id = models.PositiveSmallIntegerField(null=False, unique=True, db_column='MenuID')
    menu_name = models.CharField(null=False, max_length=30, blank=True, db_column='MenuName')
    menu_father_id = models.ForeignKey(to='self', to_field='menu_id', on_delete=models.SET_NULL, null=True,
                                       db_column='MenuFatherID')
    menu_order_no = models.CharField(max_length=20, null=False, default='999999', db_column='MenuOrderNo')
    menu_action = models.CharField(max_length=100, null=False, blank=True, db_column='MenuAction')
    menu_is_catalogue = models.BooleanField(null=False, default=False, db_column='MenuIsCatalogue',
                                            help_text='是否是目录节点')
    menu_remind_url = models.CharField(max_length=100, null=False, blank=True, db_column='MenuRemindUrl',
                                       help_text='待办提醒链接(URL)')
    menu_remind_caption = models.CharField(max_length=255, null=False, blank=True,
                                           db_column='MenuRemindCaption', help_text='待办提醒的文字描述')

    def __str__(self):
        return "{}({})".format(self.menu_name, self.menu_id)

    @staticmethod
    def root_menu_id():
        return SysMenu.objects.get(menu_father_id__isnull=True).menu_id


# 监听函数
@receiver(post_save)
def after_model_save_callback_data_doc(sender, **kwargs):
    """
    主要负责部分模型保存后的数据文件化
    """
    from apps.myerp.tools.dataDocumented import DOC_Handler
    if isinstance(kwargs['instance'], ProductCategoryPrimary):
        # 更新一级产品种类数据
        DOC_Handler['product_catagory_primary']()
        DOC_Handler['product_catagory']()
    if isinstance(kwargs['instance'], ProductCategorySecondary):
        # 更新耳机产品种类数据
        DOC_Handler['product_catagory']()
