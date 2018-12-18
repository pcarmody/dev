<html><body>
  <div id="mapdiv" style="width: 50%; float: left;">
      <div id="popup" class="ol-popup">
          <a href="#" id="popup-closer" class="ol-popup-closer"></a>
          <div id="popup-content"></div>
      </div>
  </div>
<h1>this is a header</h1>
<table>
<tbody>
<tr id="TitleRow"> </tr>
<tr id="DataRow"> </tr>
</tbody>
<table>
<div id="BottomDiv" style="clear: both;">Below</div>
  <script src="http://www.openlayers.org/api/OpenLayers.js"></script>
  <script>
    var ppp = 0;
    map = new OpenLayers.Map("mapdiv", {
        controls:[
            new OpenLayers.Control.Navigation(),
            new OpenLayers.Control.PanZoomBar(),
            new OpenLayers.Control.LayerSwitcher()
        ]
    });
    map.addLayer(new OpenLayers.Layer.OSM());

    var lonLat = new OpenLayers.LonLat(-122.365530, 37.251690) 
          .transform(
            new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
            map.getProjectionObject() // to Spherical Mercator Projection
          );
          
    var zoom=10;
    var markers = new OpenLayers.Layer.Markers( "Markers" );

//
//  define the popups
//
    function onPopupClose(evt) {
      var pops = map.popups;
      for(var a = 0; a < pops.length; a++){
         map.removePopup(map.popups[a]);
      };
    }
    function onFeatureSelect(evt) {
        feature = evt.feature;
        popup = new OpenLayers.Popup.FramedCloud("featurePopup",
                                 feature.geometry.getBounds().getCenterLonLat(),
                                 new OpenLayers.Size(100,100),
                                 "<h2>"+feature.attributes.title + "</h2>" +
                                 feature.attributes.description,
                                 null, true, onPopupClose);
        feature.popup = popup;
        popup.feature = feature;
        map.addPopup(popup);
    }
    function onFeatureUnselect(evt) {
        if (feature.popup) {
            map.removePopup(popup);
            popup.destroy();
        }
    }
    var RepeaterEntries = new Array();
    var ActiveEntries = new Array();
//    var Column2Entries = new Array();
//    var Column3Entries = new Array();

//
// add a marker 
//
    function add_freq_marker(markers, repeater) {
        var lonLat = new OpenLayers.LonLat(repeater.Lon, repeater.Lat) 
              .transform(
                new OpenLayers.Projection("EPSG:4326"), // transform from WGS 1984
                map.getProjectionObject() // to Spherical Mercator Projection
              );
        repeater.lonLat = lonLat;
        var size = new OpenLayers.Size(26,32);
        var offset = new OpenLayers.Pixel(-(size.w/2), -size.h);
//        var icon = new OpenLayers.Icon("http://maps.gstatic.com/intl/de_de/mapfiles/ms/micons/red-pushpin.png", size, offset);
        var icon = new OpenLayers.Icon(repeater.Icon, size, offset);
        marker = new OpenLayers.Marker(lonLat, icon);
        marker.events.register( 'click', markers, function () { //            feature = evt.feature;
            onPopupClose();
            ppp = new OpenLayers.Popup.FramedCloud("popup",
                                 lonLat,
                                 new OpenLayers.Size(100,100),
                                 "<h2>"+repeater.ListName +"</h2>" + 
                                 "<h3>"+repeater.CallSign+"</h3>" + 
                                 repeater.Frequency+"/"+repeater.Tone+"<br>" +
                                 "<bold>"+repeater.Comment+"</bold><br>",
//                               +  "Lon: "+repeater.Lon + " Lat: "+repeater.Lat,
                                 null, true, onPopupClose);
            map.addPopup(ppp);
        });
        
        repeater.marker = marker;
        markers.addMarker(marker);
    };
    var old_entry= 0;
    function center_on_station(marker) {
        for(i=0; i<RepeaterEntries.length; i++) {
            if(RepeaterEntries[i].lonLat == marker) {
                RepeaterEntries[i].marker.setUrl("http://127.0.0.1/repeatermap/icons/antenna_large.png");
                map.setCenter (RepeaterEntries[i].lonLat, zoom);
                if(old_entry > 0)
                    RepeaterEntries[old_entry].marker.setUrl(RepeaterEntries[old_entry].Icon);
                old_entry = i;
                markers.redraw();
                break;
            }
        }
        return RepeaterEntries[i];
    };
    function center_zoom(marker) {
        repeater = center_on_station(marker);
        map.setCenter (repeater.lonLat, zoom);
        repeater = center_on_station(marker);
        marker.events.triggerEvent("click");
    };
    
    map.setCenter (lonLat, zoom);

//
// column object definition
//

    function ColumnObject(name, file, num, titles, rows) {

      var obj = new Object();

      obj.StationList = new Array();
      obj.Name = name;
      obj.File = file;
      obj.Num = num;
      obj.Column = "Col " + name;

      obj.fill_array = function(name, file, num, column, entries) {
          var xhttp = new XMLHttpRequest();
          xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
              var Right = document.getElementById(column);
              Right.innerHTML = this.responseText;
              var arr = Right.getElementsByTagName('script')
              for (var n = 0; n < arr.length; n++)
                 eval(arr[n].innerHTML);
    //          var element = document.getElementById("ColumnDiv"+column);
              Right.innerHTML = fill_column(entries);
            };
          };
          xhttp.open("GET", "right.php?file="+file+"&column="+num+"&name="+name, true);
          xhttp.send();
      };
    
      obj.add_title = function() {
          return "<th>" + this.Name + "</th>";
      };

      obj.add_row = function() {
          return "<td id=\"Col " + name + "\" valign='top'></td>";
      };

      obj.add_station = function (station) {
           this.StationList.push(station);
      };

      titles.innerHTML += "<th>" + obj.Name + "</th>";
      rows.innerHTML += "<td id=\"" + obj.Column + "\" valign='top'></td>";

      obj.fill_array(name, file, num, obj.Column, obj.StationList);

      return obj;
    }
    function fill_column(arr) {
      var output_html = "<table>";
    
      for (var n = 0; n < arr.length; n++) {
        output_html += "<tr> <td onclick=\"center_on_station('"+
            arr[n].lonLat +
            "');\" ondblclick=\"center_zoom('" + 
            arr[n].lonLat +
            "');\">" +
            arr[n].CallSign +
    /*        "</td><td>" + 
            arr[n].Comment + */
            "</td></tr>\n";
        }
    
      output_html += "</table>";
    
      return output_html;
    };
    function fill_array(name, file, num, column, entries) {
      var xhttp = new XMLHttpRequest();
      xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
          var Right = document.getElementById(column);
          Right.innerHTML = this.responseText;
          var arr = Right.getElementsByTagName('script')
          for (var n = 0; n < arr.length; n++)
             eval(arr[n].innerHTML);
//          var element = document.getElementById("ColumnDiv"+column);
          Right.innerHTML = fill_column(entries);
        };
      };
      xhttp.open("GET", "right.php?file="+file+"&column="+num+"&name="+name, true);
      xhttp.send();
    }

    var titles = document.getElementById("TitleRow");
    var datarow = document.getElementById("DataRow");
    var ColumnObjects = new Array();
    var Favorites = ColumnObject("Favorites", " ", 1, titles, datarow);
    ColumnObjects.push(Favorites);
<?php
    $list = `ls StationLists`;
    $file_names = str_getcsv($list, "\n");
#    echo $file_names[0];
    $f = fopen("StationLists/lists.csv", "r");
    $arrays = "";
#    $titles = "<tr><th>Favorites</th>";
    $titles = "";
    $new_row = "<tr><td id='Col Favorites'></td>";
    $new_fill = "";
    $i = 0;
    while (($line = fgetcsv($f)) !== false) {
        $i = $i + 1;
        if($i == 1) {
            continue;
        }
        $new_obj = "Column".$i."Object ";
#        $titles = $titles. "<th>" . $line[0]. "</th>";
        $titles = $titles. " + " . $new_obj.".add_title()";
        $col_title = "Col ".$line[0];
        $new_row = $new_row."<td id=\"".$col_title."\" valign='top'></td>";
        $new_array = "Column".$i."Entries ";
        $arrays = $arrays. "    var ".$new_array."= new Array();\n";
#        $new_fill = $new_fill . "    fill_array(\"".$line[0]."\", \"".$line[1]."\", ".$i.", \"".$col_title."\", ".$new_array.");\n";
        $arrays = $arrays ."    var ".$new_obj." = ColumnObject(\"".$line[0]."\", \"".$line[1]."\", ".$i.", titles, datarow);\n";
        $arrays = $arrays ."    ColumnObjects.push(".$new_obj.");\n";
    }
#    $titles = $titles."</tr>\n";
    $new_row = $new_row."</tr>\n";
    $new_fill = $new_fill."";
    echo $arrays;
?>
    function loadDoc() {
//      var titles = document.getElementById("TitleRow");
 //     var titles, datarow = document.getElementById("DataRow");
//      titles.innerHTML = Favorites.add_title() <?php echo $titles; ?>;
//      for(var a = 0; a < ColumnObjects.length; a++){
//          titles.innerHTML += ColumnObjects[a].add_title();
//          titles, datarow.innerHTML += ColumnObjects[1].add_row();
//      }
<?php
      echo $new_fill;
?>

    }
    loadDoc();
</script>
</body></html>
