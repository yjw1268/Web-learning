window.onload=function(){
	var dataJsonStr=localStorage.getItem('list');
	dataJsonAll=eval('('+dataJsonStr+')');
	var dataJsonL=localStorage.getItem('userProfile');
	var dataJsonS=sessionStorage.getItem('userProfile');
	var h1=document.getElementById('visit');
	var h3=document.getElementById('userInfo');
	if(dataJsonL==null&&dataJsonS==null){
		h1.innerHTML="正在建设中！";
		h1.style.color="DarkRed";
		h3.style.color="Coral";
		}else{
			if(dataJsonL!=null){
			dataJson=eval('('+dataJsonL+')');
			}else{
			dataJson=eval('('+dataJsonS+')');
			}
		document.getElementById('userInfo').innerHTML=dataJson.userName;
		document.getElementById('userInfo').style.fontSize="46px";
		for(i=0;i<dataJsonAll.info.length;i++){
			var table=document.getElementById('tableBody');
			var _tr_ = document.createElement('tr'),
				_tduserName_ = document.createElement('td'),
				_tdemail_ = document.createElement('td'),
				_tdsignInDate_ = document.createElement('td'),
				_tdlastLoginDate_ = document.createElement('td'),
				_tdlogInTimes_ = document.createElement('td');
			_tduserName_.appendChild(document.createTextNode(dataJsonAll.info[i].userName));
			_tdemail_.appendChild(document.createTextNode(dataJsonAll.info[i].email));
			_tdsignInDate_.appendChild(document.createTextNode(dataJsonAll.info[i].signInDate));
			_tdlastLoginDate_.appendChild(document.createTextNode(dataJsonAll.info[i].lastLoginDate));
			_tdlogInTimes_.appendChild(document.createTextNode(dataJsonAll.info[i].logInTimes));
			if(dataJsonAll.info[i].userName==dataJson.userName){
				_tr_.className="table-info";
			}
			_tr_.appendChild(_tduserName_);
			_tr_.appendChild(_tdemail_);
			_tr_.appendChild(_tdsignInDate_);
			_tr_.appendChild(_tdlastLoginDate_);
			_tr_.appendChild(_tdlogInTimes_);
			table.appendChild(_tr_);
		}
	}
}

function logout(){
	r=confirm("确定要注销吗？");
	if(r==true){
	sessionStorage.removeItem('userProfile');
	location.href='index.html';
	}
}