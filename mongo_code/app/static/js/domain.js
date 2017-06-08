function rollback(id)
{
var obj=document.getElementById(id);
obj.setAttribute('style','display:none;');
var parentNode=obj.parentNode;
var td=document.createElement("td");
td.setAttribute("id", id+"edit");
td.innerHTML='<input id="version"></input><a title="保存" class="fa fa-save fa-fw" herf="javascript:void(0);" onclick="post(\'/domain/deploy/\',{domain :\''+id+'\' ,action:1})"></a><a title="取消" class="fa fa-reply-all fa-fw" herf="javascript:void(0);" onclick="cancel(\''+id+'\')"></a>';
parentNode.appendChild(td);
}

function cancel(id)
{
var obj=document.getElementById(id);
obj.setAttribute('style','');
var parentNode=obj.parentNode;
var td=document.getElementById(id+"edit");
parentNode.removeChild(td);
}

function post(url, data){
    var resultid = data["domain"]+"result";
    var obj=document.getElementById(data["domain"]);
    var a=document.createElement("a");
    a.setAttribute("id", resultid)
    obj.appendChild(a);

    document.getElementById(resultid).innerHTML='<img src="/static/images/0.gif">';

    var b = "";
    for (var x in data) {
    b = b+x+"="+data[x]+"&"
    }

    b = b.slice(0, -1);

    if(data["action"]==1) {
        var version = document.getElementById("version").value;
        cancel(data["domain"])
        b = b+"&version="+version;
    }

    var ajax;
    if(window.XMLHttpRequest){ //Mozilla 浏览器
        ajax = new XMLHttpRequest();
         
        if (ajax.overrideMimeType)
            ajax.overrideMimeType("application/json");
    }
    else if (window.ActiveXObject){ // IE浏览器
        try{
            ajax = new ActiveXObject("Msxml2.XMLHTTP");
        }
        catch (e){
            try{
                ajax = new ActiveXObject("Microsoft.XMLHTTP");
            }
            catch (e) {}
        }
    }   
     
    if (!ajax) { 
        window.alert("不能创建XMLHttpRequest对象实例.");
        return false;
    }
    

    ajax.open("post", url, true);
    ajax.setRequestHeader("contentType","text/html;charset=uft-8") 
    ajax.setRequestHeader("Content-Type","application/x-www-form-urlencoded");
    ajax.send(b);
    ajax.onreadystatechange = function(){
        if (ajax.status == 200){
        location.reload();
        }
    }
}