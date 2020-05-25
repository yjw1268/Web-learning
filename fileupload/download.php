<?php
//不支持Mac，暂时不用
ini_set("display_errors", "On");
error_reporting(E_ALL || E_STRICT);
echo("正在压缩...");
function addFileToZip($path, $zip)
{
    $handler = opendir($path); //打开当前文件夹由$path指定。   
    while (($filename = readdir($handler)) !== false) {
        if ($filename != "." && $filename != "..") { //文件夹文件名字为'.'和‘..'，不要对他们进行操作       
            if (is_dir($path . "/" . $filename)) { // 如果读取的某个对象是文件夹，则递归         
                addFileToZip($path . "/" . $filename, $zip);
            } else { //将文件加入zip对象         
                $zip->addFile($path . "/" . $filename);
            }
        }
    }
    @closedir($path);
}
$zip = new ZipArchive();
if ($zip->open('./zip/uploads.zip', ZipArchive::OVERWRITE) === TRUE) {
    addFileToZip('./uploads', $zip); //调用方法，对要打包的根目录进行操作，并将ZipArchive的对象传递给方法   
    $zip->close(); //关闭处理的zip文件 
    echo "https://www.bupt404.cn/upload/zip/uploads.zip";
    header("Content-Type: application/zip"); //zip格式的
    header("Content-Transfer-Encoding: binary"); //告诉浏览器，这是二进制文件
    header('Content-disposition:attachment;filename=uploads.zip');
    $filesize = filesize('./zip/uploads.zip');
    header('Content-length:' . $filesize);
    readfile('./zip/uploads.zip');
    // unlink('./zip/uploads.zip'); //删除文件
}
?>