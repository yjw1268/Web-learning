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
?>