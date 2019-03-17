<?php
ini_set("display_errors", "On");
error_reporting(E_ALL || E_STRICT);
echo("<title>排名查询-Powered by IMOE.CLUB</title>");
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $mode=$_POST["mode"];
    #echo $mode;
    if($mode=="1"){
        $checkmode="daily";
    }elseif($mode=="2"){
        $checkmode="weekly";
    }elseif($mode=="3"){
        $checkmode='monthly';
    }elseif($mode=='R1'){
        $checkmode='daily_r18';
    }elseif($mode=='R2'){
        $checkmode='weekly_r18';
    }else{
        echo "<title>Acess denied!</title>";
        echo "<script>alert('输入有误！');</script>";
        header("Refresh:1;url=p_rank.html");
        die("<h1>正在返回上一级页面...</h1>");
    }
    $number=$_POST["number"];
    $output=shell_exec("python3 pixiv_rank.py $mode $number");
    # echo $output;
    #echo $checkmode;
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
        echo("<center><h1>RANK</h1>"."<h3>点击图片可以查看大图哦</h3><br>");
    }
    $sql = "SELECT local_url,mode,pixiv_id,temp_rank,rank_date,title FROM pixiv_rank WHERE mode='$checkmode' AND temp_rank<'$number' AND rank_date>current_date";
    $result = mysqli_query($link, $sql);
    # 读取并输出数据
    if (mysqli_num_rows($result) > 0) {
        // 输出数据
        while($row = mysqli_fetch_assoc($result)) {
            echo "<a href='http://study.imoe.club/Try/get_pic.php?id=".$row["pixiv_id"]."'>"."<img src=".$row["local_url"]." /></a>". "<br>".$row["title"]. "<br><br>";
        }
    } else {
        echo "获取失败！请联系维护人员！"."<br>";
    }
    // mysqli_query("DELETE FROM pixiv_rank");
    echo("<h5>Powered by IMOE.CLUB</h5></center>");  
    mysqli_close($link);
}
else{
    echo "<title>Acess denied!</title>";
    echo "<h1>非法闯入！</h1>";
    header("Refresh:1;url=../index.html");
}
?>