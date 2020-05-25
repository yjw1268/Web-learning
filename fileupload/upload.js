$(document).ready(function(){
    var inputCover = $(".inputCover");
    var processNum = $(".processNum");
    var processBar = $(".processBar");
    //上传准备信息
    $("#file").change(function(){
        var file = document.getElementById('file');
        var fileName = file.files[0].name;
	var fileSize = file.files[0].size;
        processBar.css("width",0); 
        //验证要上传的文件
	if(fileSize > 1024*20*1024){
	    inputCover.html("<font>文件过大，请重新选择</font>");
	    processNum.html('未选择文件');
	    document.getElementById('file').value = '';
	    return false;
	}else{
	    inputCover.html(fileName+' / '+parseInt(fileSize/1024)+'K');
	    processNum.html('等待上传');
	}
    })
 
    //提交验证
    $(".submit").click(function(){
	if($("#file").val() == ''){
            alert('请先选择文件！');
	}else{
	    upload();
	}
    })
 
    //创建ajax对象，发送上传请求
    function upload(){
        var file = document.getElementById('file').files[0];
	var form = new FormData();
	form.append('myfile',file);
	$.ajax({
        url: 'https://www.bupt404.cn/upload/process.php',//上传地址
	    async: true,//异步
	    type: 'post',//post方式
	    data: form,//FormData数据
	    processData: false,//不处理数据流 !important
 	    contentType: false,//不设置http头 !important
 	    xhr:function(){//获取上传进度            
                myXhr = $.ajaxSettings.xhr();
                if(myXhr.upload){
                    myXhr.upload.addEventListener('progress',function(e){//监听progress事件
                    var loaded = e.loaded;//已上传
                        var total = e.total;//总大小
                        var percent = Math.floor(100*loaded/total);//百分比
                        processNum.text(percent+"%");//数显进度
                        processBar.css("width", percent + "px");//图显进度
                    }, false);
                }
                return myXhr;
            },
        success: function (data) {//上传成功回调
            processNum.text("100%");
            processBar.css("width", 100);
            console.log(data);//获取文件链接
            //document.cookie = "url="+data;//此行可忽略
            // alert("上传文件 " + data + " 成功");
            $(".submit").text('上传成功');
            $(".submit").attr("disabled", true); 
            $(".upagain").css("display", "block");
             }
	})
    }
 
    //继续上传
    $(".upagain").click(function(){
	$("#file").click();
	processNum.html('未选择文件');
        processBar.css("width",0); 
        $(".submit").text('上传');
        $(".submit").attr("disabled", false); 
	document.getElementById('file').value = '';
	$(this).css("display","none");
    })
})
