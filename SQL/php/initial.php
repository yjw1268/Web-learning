<?php
# 版本：PHP7
# 显示PHP错误信息
ini_set("display_errors", "On");
error_reporting(E_ALL || E_STRICT);
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
# 在数据库Study下创建数据表MyGuest
$sql = "CREATE TABLE SQLuser (
    id INT(6) UNSIGNED AUTO_INCREMENT PRIMARY KEY, 
    userName VARCHAR(20) NOT NULL,
    userPassword VARCHAR(20) NOT NULL,
    email VARCHAR(50),
    reg_date TIMESTAMP,
    lastLoginDate TIMESTAMP
    )"; 
if ($link->query($sql) === TRUE) {
    echo "Table MyGuests created successfully"."<br>";
} else {
    echo "创建数据表错误: " . $link->error."<br>";
}
?>