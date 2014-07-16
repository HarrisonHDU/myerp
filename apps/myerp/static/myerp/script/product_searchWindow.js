/**
 * Created by Administrator on 14-7-7.
 */
Ext.ns('Ext.ux.window');

Ext.ux.window.ProductSearchWindow = Ext.extend(Ext.Window,{
    initComponent: function(){
        Ext.ux.window.ProductSearchWindow.superclass.initComponent.call(this);
    },
    layout: 'fit',
    title: '产品查询',
    width: 500,
    height: 400,
    closeAction: 'hide',
    buttonAlign: 'center',
    border: false,
    // Required. 关联的表单字段
    formField: undefined,
    plugins: new Ext.ux.grid.ProductSearchGrid({
        url: this.url || '/myerp/sys/product_id_name/',
        pageSize: this.pageSize || 20,
        listeners: {
            rowdblclick: function(grid, rowIndex, e){
                var window = grid.ownerCt;
                var record = grid.getStore().getAt(rowIndex);
                var f = window.formField.setValue(record.get('name'));
                //this.formField.fireEvent('grid_selected', record.get('pid'), record.get('name'));
                window.hide();
            }
        }
    })
});