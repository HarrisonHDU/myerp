/**
 * Created by Administrator on 14-7-7.
 */
Ext.ns('Ext.ux.grid');

Ext.ux.grid.ProductSearchGrid = Ext.extend(Ext.grid.GridPanel,{
    pageSize: 20,
    url: '/myerp/sys/product_id_name/',
    sm: new Ext.grid.RowSelectionModel({
        singleSelect: true
    }),
    cm: new Ext.grid.ColumnModel([
        new Ext.grid.RowNumberer(),
        {header: '产品编码', dataIndex: 'pid', width: 100},
        {header: '产品名称', dataIndex: 'name', width: 150}
    ]),
    viewConfig: {
        forceFit: true
    },
    store: new Ext.data.JsonStore({
        root: 'items',
        totalProperty: 'total',
        idProperty: 'pid',
        remoteSort: true,
        sortInfo: {
            field: 'pid',
            direction: 'ASC'
        },
        fields:['pid', 'name']
    }),
    tbar: [{
        text: '查询'
    }],
    bbar: [],
    init: function(container){
        var store = this.getStore();
        Ext.apply(store, {
            proxy: new Ext.data.HttpProxy({url: this.url})
        });
        // 添加分页工具条
        this.getBottomToolbar().add({
            xtype: 'paging',
            pageSize: this.pageSize,
            displayInfo: true,
            store: store,
            // 添加分页工具条无法自适应宽度，这里暂时把宽度写死，但无法随着表格宽度变化而变化
            width: 485
        });
        store.load({params:{start:0,limit:this.pageSize}});
        container.add(this);
    }
});