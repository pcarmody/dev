<?php
function station_icon($freq, $tone) {
    $file_name = "icons/stations/" . $freq . "_" . $tone . ".png";
#    if(!file_exists($file_name)) {
        exec("rm ".$file_name);
        echo "// building ". $file_name . "\n";
        echo "// ". exec("python station_icon.py " . $freq . " " . $tone . " 2>&1"). "\n";
#        echo "python station_icon.py " . $freq . " " . $tone;
#    } else {
#        echo "//////// ". $file_name ." already exists!\n";
#    }

    return $file_name;
}

var_dump ($argv);
echo "arv 1 = ".$argv[1]. "\n";
$f = fopen($argv[1], "r");
while (($line = fgetcsv($f)) !== false) {

    if(is_numeric($line[19]) && is_numeric($line[20])) {
        station_icon($line[2], $line[6]);
    }
}
fclose($f);
?>
