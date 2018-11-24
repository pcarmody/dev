<script>
    var markers = new OpenLayers.Layer.Markers( "Markers2" );
    var RepeaterEntry = 0;
//    add_freq_marker(markers, 37.437250, -122.371140, "test");
//    map.addLayer(markers);
<?php
function str_attr($name, $value) {
    return "    RepeaterEntry.".$name."= \"".$value."\"";
}
function num_attr($name, $value) {
    return "    RepeaterEntry.".$name."= ".$value;
}
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
        echo "   var RepeaterEntry = new Object;\n"; 
        echo str_attr("CallSign", $line[1]).";\n";
        echo str_attr("Frequency", $line[2]).";\n";
        echo str_attr("Tone", $line[6]).";\n";
        echo str_attr("Comment", $line[13]).";\n";
        echo str_attr("Icon", get_icon($line[2])).";\n";
        echo num_attr("Lon", $line[20]).";\n";
        echo num_attr("Lat", $line[19]).";\n";
        echo "   add_freq_marker(markers, RepeaterEntry );\n";
        echo "   RepeaterEntries.push(RepeaterEntry);\n";
        echo "   Column".$_GET['column']."Entries.push(RepeaterEntry);\n";
#        echo "   alert(\"Column".$_GET['column']."\");\n";
    }
}
fclose($f);
?>
    map.addLayer(markers);
</script>
