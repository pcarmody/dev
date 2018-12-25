<script>
    var markers = new OpenLayers.Layer.Markers( "Markers2" );
<?php
function get_icon($freq) {
    if($freq < 140.0) {
        $color = "bullet_black.png";
    } else if($freq < 150.0) {
        $color = "bullet_red.png";
    } else if($freq < 150.0) {
        $color = "bullet_yellow.png";
    } else if($freq < 220.0) {
        $color = "bullet_green.png";
    } else if($freq < 440.0) {
        $color = "bullet_blue.png";
    } else if($freq < 460.0) {
        $color = "bullet_purple.png";
    } else {
        $color = "bullet_white.png";
    } 
     
    return "http://127.0.0.1/repeatermap/icons/".$color;
}
$f = fopen("StationLists/".$_GET["file"], "r");
while (($line = fgetcsv($f)) !== false) {

    if(is_numeric($line[19]) && is_numeric($line[20])) {
        echo "   var Station = StationObject(markers, ".
             "\"".$line[1]."\", ".
             "\"".$line[2]."\", ".
             "\"".$line[6]."\", ".
             "\"".$line[13]."\", ".
             "\"".get_icon($line[2])."\", ".
             $line[20].", ".
             $line[19].", ".
             "\"".$_GET['name']."\");\n";
        echo "   RepeaterEntries.push(Station);\n";
        echo "   Column".$_GET['column']."Object.add_station(Station);\n";
#        echo "   alert(\"Column".$_GET['column']."\");\n";
    }
}
fclose($f);
?>
    map.addLayer(markers);
</script>
