/**
 * Created by Harrison on 14-6-26.
 */

/* crsf验证 */
Ext.Ajax.on('beforerequest', function (conn, options) {
    if (!(/^http:.*/.test(options.url) || /^https:.*/.test(options.url))) {

        if(Ext.util.Cookies.get('csrftoken')==null){
            Ext.util.Cookies.set('csrftoken','csrftoken')
        }
        if (typeof(options.headers) == "undefined") {
            options.headers = {'X-CSRFToken': Ext.util.Cookies.get('csrftoken')};
        } else {
            options.headers['X-CSRFToken']=Ext.util.Cookies.get('csrftoken');
        }
    }
}, this);