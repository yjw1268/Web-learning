<?php
//使用系统自带的命令压缩
ini_set("display_errors", "On");
error_reporting(E_ALL || E_STRICT);
shell_exec("zip -r zip/uploads.zip uploads");
header("Content-Type: application/zip"); //zip格式的
header("Content-Transfer-Encoding: binary"); //告诉浏览器，这是二进制文件
header('Content-disposition:attachment;filename=uploads.zip');
$filesize = filesize('./zip/uploads.zip');
header('Content-length:' . $filesize);
readfile('./zip/uploads.zip');
unlink('./zip/uploads.zip');
?>