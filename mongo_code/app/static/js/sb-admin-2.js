$(function() {

    $('#side-menu').metisMenu();

});

//Loads the correct sidebar on window load,
//collapses the sidebar on window resize.
// Sets the min-height of #page-wrapper to window size
$(function() {
    $(window).bind("load resize", function() {
        topOffset = 50;
        width = (this.window.innerWidth > 0) ? this.window.innerWidth : this.screen.width;
        if (width < 768) {
            $('div.navbar-collapse').addClass('collapse');
            topOffset = 100; // 2-row-menu
        } else {
            $('div.navbar-collapse').removeClass('collapse');
        }

        height = ((this.window.innerHeight > 0) ? this.window.innerHeight : this.screen.height) - 1;
        height = height - topOffset;
        if (height < 1) height = 1;
        if (height > topOffset) {
            $("#page-wrapper").css("min-height", (height) + "px");
        }
    });

    var url = window.location;
    var element = $('ul.nav a').filter(function() {
        return this.href == url || url.href.indexOf(this.href) == 0;
    }).addClass('active').parent().parent().addClass('in').parent();
    if (element.is('li')) {
        element.addClass('active');
    }
});


//分页
//container 容器，count 总页数 pageindex 当前页数
function setPage(container, count, pageindex) {
  var container = container;
  var count = count;
  var pageindex = pageindex;
  var a = [];

  if (count == 0) {
      count = 1;
  }

  function setPageList() {

      if (pageindex == i) {
        a[a.length] = "<li class=\"paginate_button active\"><a href=\"#\">" + i + "</a></li>";
      } else {
        a[a.length] = "<li class=\"paginate_button\"><a href=\"?p=" + i +"\">" + i + "</a></li>";
      }
    }

    //总页数少于10 全部显示,大于10 显示前3 后3 中间3 其余....
    if (pageindex == 1) {
      a[a.length] = "<li class=\"paginate_button previous disabled\"><a href=\"#\">上一页</a></li>";
    } else {
      a[a.length] = "<li class=\"paginate_button previous\"><a href=\"?p=" + (pageindex-1) + "\">上一页</a></li>";
    }

    //总页数小于10
    if (count <= 10) {
      for (var i = 1; i <= count; i++) {
        setPageList();
      }
    }
    //总页数大于10页
    else {

      if (pageindex <= 4) {
        for (var i = 1; i <= 5; i++) {
          setPageList();
        }
        a[a.length] = "<li class=\"paginate_button\"><a>...</a></li><li class=\"paginate_button previous\"><a href=\"?p=" + count + "\">" + count + "</a></li>";
      } else if (pageindex >= count - 3) {
        a[a.length] = "<li class=\"paginate_button\"><a href=\"?p=1\">1</a></li><li class=\"paginate_button\"><a>...</a></li>";
        for (var i = count - 4; i <= count; i++) {
          setPageList();
        }
      }
      else { //当前页在中间部分
        a[a.length] = "<li class=\"paginate_button\"><a href=\"?p=1\">1</a></li><li class=\"paginate_button\"><a>...</a></li>";
        for (var i = pageindex - 2; i <= pageindex + 2; i++) {
          setPageList();
        }
        a[a.length] = "<li class=\"paginate_button\"><a>...</a></li><li class=\"paginate_button\"><a href=\"?p="+count+"\">" + count + "</a></li>";
      }

    }

    if (pageindex == count) {
      a[a.length] = "<li class=\"paginate_button next disabled\"><a href=\"#\">下一页</a></li>";
    } else {
      a[a.length] = "<li class=\"paginate_button next\"><a href=\"?p=" + (pageindex+1) + "\">下一页</a></li>";
    }
    container.innerHTML = a.join("");
}

function del(url)
  {
  var r=confirm("是否删除")
  if (r==true)
    {
    window.location.href=url;
    }
  else
    {
    pass
    }
  }