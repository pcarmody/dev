<script>
    var markers = new OpenLayers.Layer.Markers( "Markers2" );
    add_freq_marker(markers, 37.437250, -122.371140, "test");
//    map.addLayer(markers);
</script>
<?php
echo "<table>";
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
        echo "   add_freq_marker(markers, ", $line[19].", ".$line[20].", \"".$line[1]."\");";
        echo "</script>\n";
    }
}
fclose($f);
echo "</table>";
?>
<script>
    map.addLayer(markers);
</script>
