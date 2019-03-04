<?php
ini_set("display_errors", "On");
error_reporting(E_ALL || E_STRICT);
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $mode=$_POST["mode"];
    $number=$_POST["number"];
    $output=shell_exec("python3 pixiv_rank.py $mode $number");
    # echo $output;
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
        echo("Connected successfully"."<br>");
    }
    $sql = "SELECT local_url FROM pixiv_rank";
    $result = mysqli_query($link, $sql);
    # 读取并输出数据
    if (mysqli_num_rows($result) > 0) {
        // 输出数据
        while($row = mysqli_fetch_assoc($result)) {
            echo "<img src=".$row["local_url"]." />". "<br>";
        }
    } else {
        echo "0 结果"."<br>";
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