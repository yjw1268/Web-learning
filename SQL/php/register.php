<?php
ini_set("display_errors", "On");
error_reporting(E_ALL || E_STRICT);
$link=mysqli_connect("localhost","root","PlanetarAntimony","Study"); 
if (!$link){
    echo("Could not connect");
}
else{
    echo("Connected successfully"."<br>");
}
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $userName=$_POST["userName"];
    $email=$_POST["email"];
    $userPassword=$_POST["userPassword"];
    $sql = "INSERT INTO SQLuser (userName, email,userPassword)
    VALUES ('".$userName."', '".$email."', '".$userPassword."')";
    if (mysqli_query($link, $sql)){
        echo "<h2>注册成功，3秒后跳转主页</h2>"."<br>";
        echo "<h5>没有跳转？<a href='../index.html'>点这里</a></h5>";
        header("Refresh:3;url=../index.html");
    }else {
        echo "Error: " . $sql . "<br>" . mysqli_error($link)."<br>";
    }
}
mysqli_close($link);
?>