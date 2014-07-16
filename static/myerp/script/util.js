/**
 * Created by Harrison on 14-6-27.
 */

/*
    根据传入的比较函数查找数组中符合要求的元素，只返回第一个满足的元素，不存在则返回null
    比较函数返回0表示匹配成功，返回其他值表示失败
 */
Array.prototype.search = function(search_func){
    for (var i= 0; i<this.length; i++){
        if (search_func(this[i]) == 0)
            return this[i]
    }
    return null;
}