<?php
header('Access-Control-Allow-Origin:https://bupt404.cn');
header('Access-Control-Allow-Methods:GET,POST');
if(isset($_FILES["myfile"])){  
    move_uploaded_file($_FILES["myfile"]["tmp_name"],"uploads/".$_FILES["myfile"]["name"]);
    echo $_FILES["myfile"]["name"];
}else{
    echo 'No file';
}
?>