<?php

if($_GET['save']) {
echo "saved\n";
echo $_GET['save'];
    $f = fopen("favorites.json", "w") or die("unable to open file");
    fwrite($f, $_GET['save']);
    fclose($f);
}

if($_GET['load']) {
    $f = fopen("favorites.json", "r");
    echo fread($f, filesize("favorites.json"));
    fclose($f);
}

?>
