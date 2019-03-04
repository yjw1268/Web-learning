<?php
ini_set("display_errors", "On");
error_reporting(E_ALL || E_STRICT);
if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $mode=$_POST["mode"];
    $number=$_POST["number"];
    $output=shell_exec("python3 pixiv_rank.py $mode $number");
    echo $output;
}
?>