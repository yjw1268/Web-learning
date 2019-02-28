<?php
ini_set("display_errors", "On");
error_reporting(E_ALL || E_STRICT);
$link=mysqli_connect("localhost","root","PlanetarAntimony","Study"); 
// if (!$link){
//     echo("Could not connect");
// }
// else{
//     echo("Connected successfully"."<br>");
// }
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $userName=$_POST["userName"];
    $userPassword=$_POST["userPassword"];
    $sql = "SELECT userName, email
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
        $sql = "SELECT userName, email,userPassword
                FROM SQLuser
                WHERE (userName='$userName' OR email='$userName') AND userPassword='$userPassword'";
        $retval = mysqli_query( $link, $sql );
        $number=mysqli_num_rows($retval);
        if($number){
            echo "<h2>Succeed! Welcome ".$userName."!</h2><br>";
            //echo "Now：".$showtime=date("Y-m-d H:i:s");
            $h=date('H');
            if($h<6)echo '凌晨不睡的么';
            else if ($h<11) echo '早上好';
            else if ($h<13) echo '中午好';
            else if ($h<17) echo '下午好';
            else echo '<h1>晚上好</h1>';
            header("Refresh:3;url=../main.html");
        }else{
            echo "Psd error";
            header("Refresh:3;url=../index.html");
        }
    }
    else{
        echo "username not exit";
        header("Refresh:3;url=../index.html");
    }
    mysqli_free_result($retval);
}
mysqli_close($link);
?>