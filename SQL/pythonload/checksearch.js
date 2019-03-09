function check(){
    var marks=document.getElementById('marks').value;
    var getnumber = document.getElementById('getnumber').value;
    return checkmarks(marks) && checknumber(getnumber);
}

function checknumber(getnumber){
    if(isNaN(getnumber)){
        alert("输入错误");
        return false;
    }
    else if(getnumber>5){
        alert("输入错误");
        return false;
    }else if(getnumber<1){
        alert("输入错误");
        return false;
    }else{
        return true;
    }
}

function checkmarks(marks){
    if(isNaN(marks)){
        alert("输入错误1");
        return false;
    }
    else if(marks>5000){
        alert("输入错误");
        return false;
    }else if(marks<0){
        alert("输入错误");
        return false;
    }else{
        return true;
    }
}