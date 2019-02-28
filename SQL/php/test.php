<?php
ini_set("display_errors", "On");
error_reporting(E_ALL || E_STRICT);
$link=mysqli_connect("localhost","root","PlanetarAntimony","Study"); 
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $userName=$_POST["userName"];
    $sql = "SELECT userName, email,userPassword
            FROM SQLuser
            WHERE userName='$userName' OR email='$userName'";
    $retval = mysqli_query( $link, $sql );
    // if(! $retval )
    // {
    //     die('无法读取数据: ' . mysqli_error($link));
    // }
    // else{
    //     echo "读取成功";
    // }
    $number=mysqli_num_rows($retval);
    if($number){
        echo "1";
    }
    else{
        echo "0";
    }
    //echo $number;
    mysqli_free_result($retval);
}
mysqli_close($link);
?>