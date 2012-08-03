//用于 "顶/踩"无刷新实现
//memoryboxes@gmail.com
//2012-03-17


//这部分暂时不用，因为统计代码加载较慢，所以不用等到页面全部加载完毕
/*
window.onload = prepareLinks;

//为每一个顶/踩连接加入处理函数
function prepareLinks()
{
    var links = document.getElementsByTagName("a");
    for(var i = 0; i < links.length; i++)
    {
        if(links[i].getAttribute("class") == "dig like float_left")
        {
            links[i].onclick = function(){
                LikeAjaxFunction(this);
                return false;
            }
        }
        
        if(links[i].getAttribute("class") == "dig bury float_right")
        {
            links[i].onclick = function(){
                BuryAjaxFunction(this);
                return false;
            }
        }
    }
}
*/

//顶
function LikeAjaxFunction(likeNode) {
    resource_id = likeNode.parentNode.lastChild.previousSibling.childNodes[0].nodeValue
    DigAjaxFunction('like', likeNode, resource_id);
    
}

//踩
function BuryAjaxFunction(buryNode) {
    resource_id = buryNode.parentNode.lastChild.previousSibling.childNodes[0].nodeValue
    DigAjaxFunction('bury', buryNode, resource_id);
}


//创建XMLHttpRequest对象，异步处理
function DigAjaxFunction(str, elementNode, resource_id) {
    var xmlHttp;
    try {
        // Firefox, Opera 8.0+, Safari
        xmlHttp = new XMLHttpRequest();
    } catch (e) {

        // Internet Explorer
        try {
            xmlHttp = new ActiveXObject("Msxml2.XMLHTTP");
        } catch (e) {

            try {
                xmlHttp = new ActiveXObject("Microsoft.XMLHTTP");
            } catch (e) {
                alert("您的浏览器不支持AJAX！");
                return false;
            }
        }
    }

    var strpost = ""
    if(str == "like")
    {
        xmlHttp.onreadystatechange = function() {
            if(xmlHttp.readyState == 4) {
                if(xmlHttp.responseText)
                    elementNode.firstChild.nodeValue = "顶+" + xmlHttp.responseText;
            }
        }
        strpost = "?scoretype=score_like&resource_id=" + resource_id
    }
    
    else
    {
        xmlHttp.onreadystatechange = function() {
            if(xmlHttp.readyState == 4) {
                if(xmlHttp.responseText)
                    elementNode.firstChild.nodeValue = "踩+" + xmlHttp.responseText;
            }
        }
        strpost = "?scoretype=score_bury&resource_id=" + resource_id
    }
    xmlHttp.open("POST", strpost, true);
    xmlHttp.send(null);
}