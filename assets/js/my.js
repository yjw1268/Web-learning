$(document).ready(function (){
  $.getJSON("./assets/js/data1.json", function(data){
    // var $jsontip = $("#jsonTip");
    // var strHtml = "测试";
    // //存储数据的变量
    // $jsontip.empty();
    // //清空内容 
    // $.each(data, function (infoIndex, info){
    //   strHtml += "格言：" + info["content"] + "<br>";
    //   strHtml += "编码：" + info["number"] + "<br>";
    //   strHtml += "<hr>" 
    // }) 
    var x = 2300;
    var y = 200;
    var rand = parseInt(Math.random() * (x - y + 1) + y);
    $("#description").html(data[rand].content + "<br/> -「<strong>" + data[rand].number + "</strong>」");
    //$jsontip.html(strHtml);
    //显示处理后的数据
  })
})
