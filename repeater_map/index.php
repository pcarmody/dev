<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css">
  <script src="https://ajax.googleapis.com/ajax/libs/jquery/3.3.1/jquery.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.14.3/umd/popper.min.js"></script>
  <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.1.3/js/bootstrap.min.js"></script>
</head>
<body>
  <div id="mapdiv" style="width: 30%; float: left;">
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
                                 repeater.gen_popup(), 
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
// station object definition
//

    function StationObject(markers, call_sign, freq, tone, comment, icon, lon, lat, list_name) {

        var obj = new Object();
   
        obj.CallSign = call_sign;
        obj.Frequency = freq;
        obj.Tone = tone;
        obj.Comment = comment;
        obj.Icon = icon;
        obj.Lon = lon;
        obj.Lat = lat;
        obj.ListName = list_name;

        obj.gen_html = function() {

              var is_a_favorite = 0;
              var arr = Favorites.StationList;

              for (var n = 0; n < arr.length; n++) 
                  if(arr[n] == this)
                      is_a_favorite = 1;

              var text_format = "";
              if(is_a_favorite)
                  text_format = 'text-primary font-italic font-weight-bold';
               
              return "<tr><td><div class='dropdown'>" +
              "  <button type='button' class='btn btn-primary dropdown-toggle' data-toggle='dropdown'>" +
              //"    Dropdown button" +
              this.CallSign +
              "  </button>" +
              "  <div class='dropdown-menu'>" +
              "    <h3>"+this.ListName+"</h3>" +
                   "<button class='" + text_format + "'>" + this.CallSign + "</button><br>" +  
                   this.Frequency + "/" + this.Tone + "<br>" + 
                   "<bold>" + this.Comment + "</bold><br>"  +
//              "    <a class='dropdown-item' href='#'>"+this.ListName+"</a>" +
//              "    <a class='dropdown-item' href='#'>"+this.CallSign+"</a>" +
//              "    <a class='dropdown-item' href='#'>"+ this.Frequency + "/" + this.Tone + "</a>" +
//              "    <a class='dropdown-item' href='#'><bold>"+this.Comment+"</bold></a>" +
              "  </div>" +
              "</div></td></tr>";
        };

        obj.gen_popup = function() {
            return "<h2>" + this.ListName + "</h2>" + 
                   "<h3>" + this.CallSign + "</h3>" +  
                   this.Frequency + "/" + this.Tone + "<br>" + 
                   "<bold>" + this.Comment + "</bold><br>"; 
        };

        add_freq_marker(markers, obj);

        return obj;
    };

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

      obj.fill_column = function() {
          var output_html = "<table>";
    
          for (var n = 0; n < obj.StationList.length; n++) {
            output_html += obj.StationList[n].gen_html();
          }
    
          output_html += "</table>";
    
          return output_html;
      }

      obj.redraw_column = function(response) {
          var Right = document.getElementById(obj.Column);
          Right.innerHTML = response;
          var arr = Right.getElementsByTagName('script')
          for (var n = 0; n < arr.length; n++)
              eval(arr[n].innerHTML);
          Right.innerHTML = obj.fill_column(obj.StationList); 
      };

      obj.fill_array = function(name, file, num, entries) {
          var xhttp = new XMLHttpRequest();
          xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                obj.redraw_column(this.responseText);
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
           station.parent_index = this.StationList.length;
           station.parent_array = "Column" + this.Num + "Object";
           this.StationList.push(station);
           if(this.StationList.length < 2)
               Favorites.add_station(station);
      };

      titles.innerHTML += "<th>" + obj.Name + "</th>";
      rows.innerHTML += "<td id=\"" + obj.Column + "\" valign='top'></td>";

      obj.fill_array(name, file, num, obj.StationList);

      return obj;
    };

    function fill_column(arr) {
      var output_html = "<table>";
    
      for (var n = 0; n < arr.length; n++) {
        output_html += arr[n].gen_html();
      }
    
      output_html += "</table>";
    
      return output_html;
    };

    var titles = document.getElementById("TitleRow");
    var datarow = document.getElementById("DataRow");
    var ColumnObjects = new Array();
    var Favorites = ColumnObject("Favorites", " ", 1, titles, datarow);
    ColumnObjects.push(Favorites);

//
// redefine add_station for Favorites
//

    Favorites.add_station = function (station) {
//           station.array_index = this.StationList.length;
//           station.parent_array = "Column" + this.Column + "Object";
        this.StationList.push(station);
        this.redraw_column(" ");
    };
<?php
    $list = `ls StationLists`;
    $file_names = str_getcsv($list, "\n");
#    echo $file_names[0];
    $f = fopen("StationLists/lists.csv", "r");
    $arrays = "";
    $i = 0;
    while (($line = fgetcsv($f)) !== false) {
        $i = $i + 1;
        if($i == 1) {
            continue;
        }
        if($i >= 8) {
            break;
        }
        $new_obj = "Column".$i."Object ";
        $arrays = $arrays ."    var ".$new_obj." = ColumnObject(\"".$line[0]."\", \"".$line[1]."\", ".$i.", titles, datarow);\n";
        $arrays = $arrays ."    ColumnObjects.push(".$new_obj.");\n";
    }
    echo $arrays;
?>
</script>
</body></html>
