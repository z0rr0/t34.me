#!/usr/bin/php5

<?php
$url = "http://ya.ru";
$short = file_get_contents("http://t34.me/api/?u=".$url);
echo $short
?>