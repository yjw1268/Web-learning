<?php
ini_set("display_errors", "On");
error_reporting(E_ALL || E_STRICT);
echo("<title>文件提交列表</title>");
$dir="uploads";
$list = scandir($dir);
$list = array_diff($list,[".",".."]);
echo "<pre>";
print_r(array_merge($list));
echo "</pre><br>";
echo "已提交文件数:".count($list);
echo("<br>");
if(count($list)){
    echo ("<a href='https://www.bupt404.cn/upload/zip.php'>点击打包下载</a>");
}else{
    echo("没有文件可以下载~");
};
echo('<br><h4>清除数据</h4><form name="input" action="clear.php" method="post">密码：<input type="password" name="psd"><input type="submit" value="验证"></form>');
?>