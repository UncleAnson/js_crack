//header勾子
var code = function(){
var org = window.XMLHttpRequest.prototype.setRequestHeader;
window.XMLHttpRequest.prototype.setRequestHeader = function(key,value){
    if(key=='Origin'){ // Authorization
        debugger;
    }
    return org.apply(this,arguments);
}
}
var script = document.createElement('script');
script.textContent = '(' + code + ')()';
(document.head||document.documentElement).appendChild(script);
script.parentNode.removeChild(script);