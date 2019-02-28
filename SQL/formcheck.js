function checkForm(){ 
    var nametip = checkUserName(); 
    var emailtip = checkEmail();
    var passtip = checkPassword();  
    var conpasstip = confirmPassword(); 
    return nametip && passtip && conpasstip && emailtip; 
} 

// function submitForm(){
// 	var username=document.getElementById('userName');
// 	$.post("./php/test.php",
// 	{
// 		username:username
// 	},
// 	function(data){
// 	  alert("数据：" + data);
// 	});
// 	return false;
// }

function checkUserName(){
	//初始化list
	//取出用户名并初始化模式
	var username=document.getElementById('userName');
	var errname = document.getElementById('errName'); 
	var pattern = /^[\u4E00-\u9FA5A-Za-z0-9_]{3,15}$/;
	if(username.value.length == 0){ 
    errname.innerHTML="用户名不能为空";
    errname.className="error";
    return false; 
	}
	if(!pattern.test(username.value)){ 
    errname.innerHTML="用户名不合规范";
    errname.className="error";
    return false; 
	}
	else{ 
    errname.innerHTML="OK";
    errname.className="success"; 
    return true; 
    } 
	// if(repeat==1){
	// errname.innerHTML="用户名已被占用";
	// errname.className="error";
	// return false;
	// }
    // else{ 
    // errname.innerHTML="OK";
    // errname.className="success"; 
    // return true; 
    // } 
}
function checkEmail(){
	//取出用户名并初始化模式
	var email=document.getElementById('email');
	var erremail=document.getElementById('errEmail');
	var pattern=/^(\w)+(\.\w+)*@(\w)+((\.\w+)+)$/;
	//取出已注册的用户名并比较
	var dataJsonStr=localStorage.getItem('list');
	dataJson=eval('('+dataJsonStr+')');
	var repeat=null;
	if(email.value.length == 0){ 
    erremail.innerHTML="电子邮箱不能为空"
    erremail.className="error"
    return false; 
    }
	if(!pattern.test(email.value)){ 
    erremail.innerHTML="电子邮箱不合规范，请检查您是否输入正确"
    erremail.className="error"
    return false; 
    }
	// if(repeat==1){
	// erremail.innerHTML="邮箱已被注册";
	// erremail.className="error";
	// return false;
	// }
    else{ 
    erremail.innerHTML="OK"
    erremail.className="success"; 
    return true; 
    } 
}

function checkPassword(){ 
    var userpasswd = document.getElementById('userPassword'); 
    var errpasswd = document.getElementById('errPassword'); 
    var pattern = /(?=.*[0-9])(?=.*[a-zA-Z]).{8,30}/; 
    if(userpasswd.value.length == 0){ 
    errpasswd.innerHTML="密码不能为空"
    errpasswd.className="error"
    return false; 
    }
    else if(!pattern.test(userpasswd.value)){ 
    errpasswd.innerHTML="密码不合规范"
    errpasswd.className="error"
    return false; 
    } 
    else{ 
    errpasswd.innerHTML="OK"
    errpasswd.className="success"; 
    return true; 
    } 
} 
function confirmPassword(){ 
    var userpasswd = document.getElementById('userPassword'); 
    var userConPassword = document.getElementById('userConfirmPassword'); 
    var errConPasswd = document.getElementById('errConPass'); 
    if((userpasswd.value)!=(userConPassword.value) || userConPassword.value.length == 0){ 
    errConPasswd.innerHTML="密码不一致"
    errConPasswd.className="error"
    return false; 
    } 
    else{ 
    errConPasswd.innerHTML="OK";
    errConPasswd.className="success"; 
    return true; 
    }    
} 