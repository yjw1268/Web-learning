function checkForm(){ 
    var nametip = checkUserName(); 
    var passtip = checkPassword();  
    return (nametip && passtip); 
} 

function checkUserName(){
	//取出用户名并初始化模式
	var username=document.getElementById('userName');
	var errname = document.getElementById('errName'); 
	//取出已注册的用户名并比较
	if(username.value.length == 0){ 
    errname.innerHTML="用户名/电子邮箱不能为空";
    errname.className="error";
    return false; 
	}else if(username.value.length < 3){
        errname.innerHTML="用户名/电子邮箱格式不正确";
        errname.className="error";
        return false; 
    }else{
        errname.innerHTML="OK";
        errname.className="success"; 
        return true;
    }
}

function checkPassword(){ 
    var userpasswd = document.getElementById('userPassword'); 
    var errpasswd = document.getElementById('errPassword'); 
    if(userpasswd.value.length == 0){ 
    errpasswd.innerHTML="密码不能为空";
    errpasswd.className="error";
    return false; 
    }
    else if(username.value.length < 8){
        errname.innerHTML="密码格式不正确";
        errname.className="error";
        return false; 
    }else{
        return true
    }
} 