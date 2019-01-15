<script>
    var markers = new OpenLayers.Layer.Markers( "Markers2" );
<?php
function get_icon($freq, $tone) {
#    if($freq < 140.0) {
#        $color = "bullet_black.png";
#    } else if($freq < 150.0) {
#        $color = "bullet_red.png";
#    } else if($freq < 150.0) {
#        $color = "bullet_yellow.png";
#    } else if($freq < 220.0) {
#        $color = "bullet_green.png";
#    } else if($freq < 440.0) {
#        $color = "bullet_blue.png";
#    } else if($freq < 460.0) {
#        $color = "bullet_purple.png";
#    } else {
#        $color = "bullet_white.png";
#    } 
#     
#    return "http://127.0.0.1/repeatermap/icons/".$color;
    return "http://127.0.0.1/repeatermap/icons/stations/".$freq."_".$tone.".png";
#    return "/repeatermap/icons/station/".$freq."_".$tone.".png";
}

function station_icon($freq, $tone) {
    $file_name = "icons/stations/" . $freq . "_" . $tone . ".png";
    if(!file_exists($file_name)) {
        echo "// building ". $file_name . "\n";
        echo "// ". exec("python station_icon.py " . $freq . " " . $tone . " 2>&1"). "\n";
#        echo "python station_icon.py " . $freq . " " . $tone;
    }

    return $file_name;
}

$f = fopen("StationLists/".$_GET["file"], "r");
while (($line = fgetcsv($f)) !== false) {

    if(is_numeric($line[19]) && is_numeric($line[20])) {
#        station_icon($line[2], $line[6]);
        $col_name = "Column".$_GET['column']."Object";
        echo "   var Station = StationObject(markers, ".
             "\"".$line[1]."\", ".
             "\"".$line[2]."\", ".
             "\"".$line[6]."\", ".
             "\"".$line[13]."\", ".
             "\"".get_icon($line[2], $line[6])."\", ".
             $line[20].", ".
             $line[19].", ".
#             "\"".$_GET['name']."\");\n";
             $col_name.");\n";
        echo "   RepeaterEntries.push(Station);\n";
#        echo "   Column".$_GET['column']."Object.add_station(Station);\n";
        echo "   ".$col_name.".add_station(Station);\n";
#        echo "   alert(\"Column".$_GET['column']."\");\n";
    }
}
fclose($f);
echo "   Column".$_GET['column']."Object.sort_by_distance();\n";
?>
    map.addLayer(markers);
</script>
