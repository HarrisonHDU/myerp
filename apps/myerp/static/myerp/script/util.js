/**
 * Created by Harrison on 14-6-27.
 */

var bodyMask= null;
Ext.onReady(function(){
    bodyMask = new Ext.LoadMask(Ext.getBody(),{
        msg: '系统正在拼命处理数据，请稍等...'
    });
});





/*
 根据传入的比较函数查找数组中符合要求的元素，只返回第一个满足的元素，不存在则返回null
 比较函数返回0表示匹配成功，返回其他值表示失败
 */
Array.prototype.search = function (search_func) {
    for (var i = 0; i < this.length; i++) {
        if (search_func(this[i]) == 0)
            return this[i]
    }
    return null;
}


/*
 扩展Ext.util.Format
 */
/**
 * Format a number as CHN currency
 * @param {Number/String} value The numeric value to format
 * @return {String} The formatted currency string
 */
Ext.util.Format.chnMoney = function (v) {
    v = (Math.round((v - 0) * 100)) / 100;
    v = (v == Math.floor(v)) ? v + ".00" : ((v * 10 == Math.floor(v * 10)) ? v + "0" : v);
    v = String(v);
    var ps = v.split('.'),
        whole = ps[0],
        sub = ps[1] ? '.' + ps[1] : '.00',
        r = /(\d+)(\d{3})/;
    while (r.test(whole)) {
        whole = whole.replace(r, '￥1' + ',' + '￥2');
    }
    v = whole + sub;
    if (v.charAt(0) == '-') {
        return '-￥' + v.substr(1);
    }
    return "￥" + v;
}


doAjax = function(cfg){
    bodyMask.show();
    Ext.Ajax.request({
        url: cfg.url,
        method: cfg.method || 'POST',
        params: cfg.params || {},
        success: cfg.success || function(response, opts){
            var obj = Ext.decode(response.responseText);
            Ext.Msg.alert('成功', obj.msg);
        },
        failure: cfg.failure || function(response, opts){
            var obj = Ext.decode(response.responseText);
            Ext.Msg.alert('失败', obj.msg);
        },
        callback: cfg.callback || function(){
            bodyMask.hide();
        }
    });
}