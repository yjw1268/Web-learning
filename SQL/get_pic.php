<?php
ini_set("display_errors", "On");
error_reporting(E_ALL || E_STRICT);
if ($_SERVER["REQUEST_METHOD"] == "GET") {
    $pixiv_id=$_GET["id"];
    $urlname="http://study.imoe.club/Try/search_pic/". $pixiv_id . ".jpg";
    $filename='./search_pic/'.$pixiv_id . ".jpg";
    if(file_exists($filename)) {
        echo "The file already exists";
        header("Refresh:1;url=$filename");
    }else {
        $output=shell_exec("python3 get_pic.py $pixiv_id");
        #echo $output;
        echo "获取成功！";
        header("Refresh:1;url=$urlname");
    }
}else{
    echo "<title>Acess denied!</title>";
    echo "<h1>非法闯入！</h1>";
    # header("Refresh:1;url=../index.html");
}
?>