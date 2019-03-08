<?php
ini_set("display_errors", "On");
error_reporting(E_ALL || E_STRICT);
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $searchword=$_POST["searchword"];
    $marks=$_POST["marks"];
    $getnumber=$_POST["getnumber"];
    #$spage=$_POST["spage"];
    $spage='1';
    $output=shell_exec("python3 pixiv_search.py $searchword $marks $getnumber $spage");
    echo $output;
    # echo $checkmode;
    # 初始化数据
    $servername = "localhost";
    $username = "root";
    $password = "PlanetarAntimony";
    $dbname = "Study";
    # 连接数据库
    $link=mysqli_connect($servername,$username,$password,$dbname); 
    if (!$link){
        die("Connection failed: " . mysqli_connect_error())."<br>";
    }
    else{
        echo("Connected successfully."."<br>");
    }
    $sql = "SELECT searchword,local_url,pixiv_id FROM pixiv_search WHERE searchword='$searchword'";
    $result = mysqli_query($link, $sql);
    # 读取并输出数据
    if (mysqli_num_rows($result) > 0) {
        // 输出数据
        while($row = mysqli_fetch_assoc($result)) {
            echo "<a href='http://study.imoe.club/Try/get_pic.php?id=".$row["pixiv_id"]."'>"."<img src=".$row["local_url"]." /></a>". "<br>". "<br>";
        }
    } else {
        echo "获取失败！"."<br>";
    }
    // mysqli_query("DELETE FROM pixiv_rank");
    mysqli_close($link);
}
else{
    echo "<title>Acess denied!</title>";
    echo "<h1>非法闯入！</h1>";
    header("Refresh:1;url=../index.html");
}
?>