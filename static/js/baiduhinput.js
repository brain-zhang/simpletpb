//手写板调用
//memoryboxes@gmail.com
//2012-03-22
window.onload = function(){
    alert("hello");
    var w = window,d = document,n = navigator,k = d.f.wd
    if (w.attachEvent) {
    w.attachEvent("onload", function() {k.focus();})
    } else {
    w.addEventListener('load', function() {k.focus()},true)
    };
    var hw = {};
    hw.i = d.getElementById("sx");
    var il = false;
    if (/msie (\d+\.\d)/i.test(n.userAgent)) {
    hw.i.setAttribute("unselectable", "on")
    } else {
    var sL = k.value.length;
    k.selectionStart = sL;
    k.selectionEnd = sL
    }
    hw.i.onclick = function(B) {
    var B = B || w.event;
    B.stopPropagation ? B.stopPropagation() : (B.cancelBubble = true);
    if (d.selection && d.activeElement.id && d.activeElement.id == "kw") {
    hw.hasF = 1
    } else {
    if (!d.selection) {
    hw.hasF = 1
    }
    }
        if (!il) {
        var A = d.createElement("script");
        A.setAttribute("src", "http://www.baidu.com/hw/hwInput.js");
        d.getElementsByTagName("head")[0].appendChild(A);
        il = true;
        }
    };
}