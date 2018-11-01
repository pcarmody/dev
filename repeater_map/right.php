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
$f = fopen("newmaster3.csv", "r");
while (($line = fgetcsv($f)) !== false) {

        echo "<tr>";
        echo "<td>" . htmlspecialchars($line[1]) . "</td>";
        echo "<td>" . htmlspecialchars($line[2]) . "</td>";
        echo "<td>" . htmlspecialchars($line[6]) . "</td>";
        echo "<td>" . htmlspecialchars($line[13]) . "</td>";
#        foreach ($line as $cell) {
#                echo "<td>" . htmlspecialchars($cell) . "</td>";
#        }
        echo "</tr>\n";
    if(is_numeric($line[19]) && is_numeric($line[20])) {
        echo "<script>\n";
        echo "   var RepeaterEntry = new Object;\n"; 
        echo str_attr("CallSign", $line[1]).";\n";
        echo str_attr("Frequency", $line[2]).";\n";
        echo str_attr("Tone", $line[6]).",\n";
        echo str_attr("Comment", $line[13]).";\n";
        echo num_attr("Lon", $line[20]).";\n";
        echo num_attr("Lat", $line[19]).";\n";
#        echo "   };\n";
#        echo "   add_freq_marker(markers, ".$line[19].", ".$line[20].", \"".$line[1]."\", RepeaterEntry );\n";
        echo "   add_freq_marker(markers, RepeaterEntry );\n";
        echo "</script>\n";
    }
}
fclose($f);
?>
</table>
<script>
    map.addLayer(markers);
</script>
