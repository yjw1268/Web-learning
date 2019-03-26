<?php
ini_set("display_errors", "On");
error_reporting(E_ALL || E_STRICT);
echo("<title>ID查询-Powered by IMOE.CLUB</title>");
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $pid=$_POST["pid"];
    $output=shell_exec("python3 getid_pic.py $pid");
    $urlname="http://study.imoe.club/Try/id_pic/". $pid . ".jpg";
    echo("<center><img src=".$urlname." />");
    echo("<h5>Powered by IMOE.CLUB</h5></center>");  
    mysqli_close($link);
}
else{
    echo "<title>Acess denied!</title>";
    echo "<h1>非法闯入！</h1>";
    header("Refresh:1;url=../index.html");
}
?>