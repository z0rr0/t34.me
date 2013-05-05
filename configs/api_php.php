#!/usr/bin/php5

<?php
if (count($argv) < 2) {
    echo "Error, usage: ".$argv[0]." <your url>\n";
    exit(1);
}
$url = $argv[1];
$short = file_get_contents("http://t34.me/api/?u=".$url);
echo $short;
echo "\n"
?>
