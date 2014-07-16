/**
 * Created by Administrator on 14-7-8.
 */
Ext.ns('Ext.ux.form');

Ext.ux.form.ComboSearchField = Ext.extend(Ext.form.ComboBox, {
    initComponent : function(){
        Ext.ux.form.ComboSearchField.superclass.initComponent.call(this);

        this.triggerConfig = {
            tag:'span', cls:'x-form-twin-triggers', cn:[
            {tag: "img", src: Ext.BLANK_IMAGE_URL, cls: "x-form-trigger " + this.triggerClass},
            {tag: "img", src: Ext.BLANK_IMAGE_URL, cls: "x-form-trigger " + this.trigger2Class}
        ]};
    },

    getTrigger : function(index){
        return this.triggers[index];
    },

    initTrigger : function(){
        var ts = this.trigger.select('.x-form-trigger', true);
        this.wrap.setStyle('overflow', 'hidden');
        var triggerField = this;
        ts.each(function(t, all, index){
            t.hide = function(){
                var w = triggerField.wrap.getWidth();
                this.dom.style.display = 'none';
                triggerField.el.setWidth(w-triggerField.trigger.getWidth());
            };
            t.show = function(){
                var w = triggerField.wrap.getWidth();
                this.dom.style.display = '';
                triggerField.el.setWidth(w-triggerField.trigger.getWidth());
            };
            var triggerIndex = 'Trigger'+(index+1);

            if(this['hide'+triggerIndex]){
                t.dom.style.display = 'none';
            }
            //this.mon(t, 'click', this['on'+triggerIndex+'Click'], this, {preventDefault:true});
	       //定义第一个trigger的触发事件
            if(index==0)
            	t.on("click", this['onTriggerClick'], this, {preventDefault:true});
	       //定义第二个trigger的触发事件
            if(index==1)
            	t.on("click", this['onTrigger2Click'], this, {preventDefault:true});
            t.addClassOnOver('x-form-trigger-over');
            t.addClassOnClick('x-form-trigger-click');
        }, this);
        this.triggers = ts.elements;
    },

    validationEvent:false,
    validateOnBlur:false,
    trigger2Class:'x-form-search-trigger',
    width:180,
    hasSearch : false,
    paramName : 'query',

    onTrigger2Click : Ext.emptyFn
});

Ext.reg('combosearch', Ext.ux.form.ComboSearchField);
