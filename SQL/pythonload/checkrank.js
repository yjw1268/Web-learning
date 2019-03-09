function check(){
    var mode=document.getElementById('mode');
    var number = document.getElementById('number').value;
    if(isNaN(number)){
        alert("输入错误");
        return false;
    }
    else if(number>5){
        alert("输入错误");
        return false;
    }else if(number<1){
        alert("输入错误");
        return false;
    }else{
        return true;
    }
}