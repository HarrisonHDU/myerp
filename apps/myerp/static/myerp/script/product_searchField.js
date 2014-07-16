/**
 * Created by Administrator on 14-7-7.
 */

Ext.ns('Ext.ux.form');

Ext.ux.form.ProductSearchField = Ext.extend(Ext.form.TwinTriggerField, {
    initComponent: function(){
        Ext.ux.form.ProductSearchField.superclass.initComponent.call(this);
    },
    validateOnBlur: false,
    validationEvent: false,
    trigger2Class: 'x-form-search-trigger',
    search_type: 'id',
    queryName: 'query',
    // Required. 查询窗口
    searchWindow: undefined,
    onTrigger1Click: function(e){
    },

    onTrigger2Click: function(e){
        this.searchWindow.formField = this;
        this.searchWindow.show(this.el);
        this.setValue('a');
    }
});

Ext.reg('productSearchField', Ext.ux.form.ProductSearchField);