/**
 * Created by Administrator on 14-7-1.
 */

// 封装的ComboBoxTree组件
Ext.ux.ComboBoxTree = Ext.extend(Ext.form.ComboBox, {
    initComponent: function(){
        Ext.ux.ComboBoxTree.superclass.initComponent.call(this);

        this.treeId = Ext.id() + '-tree';
        this.maxHeight = this.maxHeight || this.height;
        this.tpl = new Ext.Template('' +
            '<tpl for=".">' +
            '<div style="height:' + this.maxHeight + 'px">' +
            '<div id="' + this.treeId + '">' +
            '</div>' +
            '</div>' +
            '</tpl>');
        this.store = new Ext.data.SimpleStore({fields: [], data: [
            []
        ]});
        this.selectedClass = this.selectedClass || '';
        // mode 必须是local,因为下拉树的数据源不再由combobox负责,而是由tree负责
        this.mode = 'local';
        this.emptyText = this.emptyText || "请选择...";
        this.triggerAction = 'all';
        this.onSelect = Ext.emptyFn;
        this.editable = false;
        this.beforeBlur = Ext.emptyFn;
        //all:所有结点都可选中
        //exceptRoot：除根结点，其它结点都可选（默认）
        //folder:只有目录（非叶子和非根结点）可选
        //leaf：只有叶子结点可选
        this.selectNodeModel = this.selectNodeModel || 'exceptRoot';
        this.addEvents('afterchange');
        this.tree = this.tree || new Ext.tree.TreePanel({
            rootVisible: false,
            loadingText: this.loadingText || '加载中...',
            loader: this.treeLoader || new Ext.tree.TreeLoader({
                dataUrl: this.dataUrl
            }),
            root: new Ext.tree.AsyncTreeNode({
                id: '0',
                text: 'root'
            })
        });
    },
    expand: function () {
        Ext.ux.ComboBoxTree.superclass.expand.call(this);
        if (this.tree.rendered) {
            return;
        }

        Ext.apply(
            this.tree, {
                height: this.maxHeight,
                width: (this.listWidth || this.width - (Ext.isIE ? 3 : 0)) - 2,
                border: false, autoScroll: true
            });
        if (this.tree.xtype) {
            this.tree = Ext.ComponentMgr.create(this.tree, this.tree.xtype);
        }
        this.tree.render(this.treeId);

        var root = this.tree.getRootNode();
        if (!root.isLoaded())
            root.reload();

        this.tree.on('click', function (node) {
            var selModel = this.selectNodeModel;
            var isLeaf = node.isLeaf();

            if ((node == root) && selModel != 'all') {
                return;
            } else if (selModel == 'folder' && isLeaf) {
                return;
            } else if (selModel == 'leaf' && !isLeaf) {
                return;
            }

            var oldNode = this.getNode();
            if (this.fireEvent('beforeselect', this, node, oldNode) !== false) {
                this.setValue(node);
                this.collapse();

                this.fireEvent('select', this, node, oldNode);
                (oldNode !== node) ?
                    this.fireEvent('afterchange', this, node, oldNode) : '';
            }
        }, this);
    },
    // private method
    // 重写onViewClick，使展开树结点是不关闭下拉框
    onViewClick: function (doFocus) {
        var index = this.view.getSelectedIndexes()[0], s = this.store, r = s.getAt(index);
        if (r) {
            this.onSelect(r, index);
        } else if (s.getCount() === 0) {
            this.collapse();
        }
        if (doFocus !== false) {
            this.el.focus();
        }
    },
    setValue: function (node) {
        this.node = node;
        var text = node.text;
        this.lastSelectionText = text;
        if (this.hiddenField) {
            this.hiddenField.value = node.id;
        }
        Ext.form.ComboBox.superclass.setValue.call(this, text);
        this.value = node.id;
    },

    defaultValue: function (v, r) {
        this.lastSelectionText = r;
        if (this.hiddenField) {
            this.hiddenField.value = v;
        }
        Ext.form.ComboBox.superclass.setValue.call(this, r);
        this.value = v;
        return this;
    },

    getValue: function () {
        return typeof this.value != 'undefined' ? this.value : '';
    },

    getNode: function () {
        return this.node;
    },
    clearValue: function () {
        Ext.ux.ComboBoxTree.superclass.clearValue.call(this);
        this.node = null;
    },

    // private
    destroy: function () {
        Ext.ux.ComboBoxTree.superclass.destroy.call(this);
        Ext.destroy([this.node, this.tree]);
        delete this.node;
    },
    getNodeById: function(id){
        return this.tree.getNodeById(id);
    },
    selectById: function(id, text){
        if (this.tree.rendered)
            this.setValue(this.tree.getNodeById(id));
        else{
            // 下拉树还没渲染，只能假选中
            this.lastSelectionText = text;
            if (this.hiddenField) {
                this.hiddenField.value = id;
            }
            Ext.form.ComboBox.superclass.setValue.call(this, text);
            this.value = id;
        }
    }
});

Ext.reg('combotree', Ext.ux.ComboBoxTree);
