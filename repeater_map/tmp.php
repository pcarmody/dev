<script>
    var markers = new OpenLayers.Layer.Markers( "Markers2" );
    var RepeaterEntry = 0;
//    add_freq_marker(markers, 37.437250, -122.371140, "test");
//    map.addLayer(markers);
</script>
<table>
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
$parts = parse_url($url);
parse_str($parts['query'], $query);
echo "file = ".$_GET["file"]
?>
</table>
<script>
    map.addLayer(markers);
</script>
