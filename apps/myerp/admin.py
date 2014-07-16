from django.contrib import admin
from apps.myerp.models import SysMenu, ProductCategoryPrimary, ProductCategorySecondary, Product, \
    Employee

# Register your models here.


class SysMenuAdmin(admin.ModelAdmin):
    list_display = ('menu_id', 'menu_name', 'menu_father_id', 'menu_action', 'menu_is_catalogue', 'is_delete')
    ordering = ('menu_id',)
    #filter_horizontal = ('menu_father_id',)


class ProductCategoryPrimaryAdmin(admin.ModelAdmin):
    list_display = ('pcid', 'name', 'is_delete')


class ProductCategorySecondaryAdmin(admin.ModelAdmin):
    list_display = ('pcid', 'pcpid', 'name', 'is_delete')


class ProductAdmin(admin.ModelAdmin):
    list_display = ('pid', 'sec_id', 'name', 'create_date', 'is_delete')


class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('eid', 'sex', 'user')


admin.site.register(SysMenu, SysMenuAdmin)
admin.site.register(ProductCategoryPrimary, ProductCategoryPrimaryAdmin)
admin.site.register(ProductCategorySecondary, ProductCategorySecondaryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Employee, EmployeeAdmin)
