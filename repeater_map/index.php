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
<h1 id='Active Station'>this is a header</h1>
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

    var GPSlon = -122.365530;
    var GPSlat = 37.251690; 
//    var GPSlonLat = new OpenLayers.LonLat(-122.365530, 37.251690) 
    var GPSlonLat = new OpenLayers.LonLat(GPSlon, GPSlat)
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
    function center_zoom(repeater) {
//        repeater = center_on_station(marker);
        map.setCenter (repeater.lonLat, zoom);
//        center_on_station(marker);
        repeater.marker.events.triggerEvent("click");
    };
    
    map.setCenter (GPSlonLat, zoom);

//
// station object definition
//

var Geographic  = new OpenLayers.Projection("EPSG:4326"); 
var Mercator = new OpenLayers.Projection("EPSG:900913");

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

    //This function takes in latitude and longitude of two location and returns the distance between them as the crow flies (in km)

    var GPSlon = -122.365530;
    var GPSlat = 37.251690; 
        obj.Distance = function() {
        var point1 = new OpenLayers.Geometry.Point(this.Lon, this.Lat).transform(Geographic, Mercator);
        var point2 = new OpenLayers.Geometry.Point(GPSlon, GPSlat).transform(Geographic, Mercator);       
//        var point2 = new OpenLayers.Geometry.Point(GPSlonLat.lon, GPSlonLat.lat).transform(Geographic, Mercator);       
            retval = point1.distanceTo(point2) * 0.61 / 1000.0;
//            return retval.toFixed(2) + " miles";
            return retval;//.toFixed(2) + " miles";
//            return point2;
        };

        obj.array_string = function() {
           return this.parent_array + "[" + this.parent_index + "]";
        };

        obj.toggle_skip = function() {

            this.skip_scan = (this.skip_scan)? 0 : 1;

        };

        obj.gen_html = function() {

            var is_a_favorite = 0;
            var arr = Favorites.StationList;

            for (var n = 0; n < arr.length; n++) 
                if(arr[n] == this)
                    is_a_favorite = 1;

            var button_type = "btn-light ";
            var text_format = "";
            var on_click = "Favorites.add_station("+this.array_string()+");";
            if(is_a_favorite) {
                text_format = 'text-primary font-italic font-weight-bold';
                on_click = "Favorites.remove_station("+this.array_string()+");";
            }

            if(!this.in_range)
                button_type += "font-italic text-info";

            var call_sign_button = "<a class='' href='javascript: " +  on_click + "'>" + 
                       "<div class='font-weight-bold'>" + this.CallSign +  "</div>" +
                   "</a>";

            var skip_button = "<a class='btn-light' href='javascript: " + this.array_string() + ".toggle_skip();'>";
            if(this.skip_scan)
                skip_button += 'scan';
            else
                skip_button += "skip";
            skip_button += "</a>";  

            var map_button = "<a class='btn-light' href='javascript: center_zoom(" + this.array_string() + ");'>map</a>";
//            var map_button = "<a class='btn-light' href='javascript: alert(\"qqqq\");'>map</a>";
//              "    <a class='dropdown-item' href='#'>"+this.ListName+"</a>" +
             
            return "<tr><td><div class='dropdown'>" +
              "  <button type='button' class='btn " + button_type + " dropdown-toggle' data-toggle='dropdown'>" +
              this.CallSign +
              "  </button>" +
              "  <div class='dropdown-menu'>" +
              "    <h3>"+this.ListName+"</h3>" +
                   call_sign_button + skip_button + " " + map_button + "<br>" +
//                   "<button class=' onclick='" +  on_click + "'>" + 
//                       "<div class='font-weight-bold'>" + this.CallSign +  "</div>" +
//                   "</button><button>button</button><br>" +  
                   this.Frequency + "/" + this.Tone + "<br>" + 
                   "<div class='font-weight-bold'>" + this.Comment + "</div><br>"  +
                this.Distance().toFixed(2) + " miles"; + 
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
                   "<bold>" + this.Comment + "</bold><br>" +
                this.Distance().toFixed(2) + " miles"; 
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
    
          for (var n = 0; n < this.StationList.length; n++) {

              if(this.StationList[n].Distance() > 40.0) {
                  this.StationList[n].in_range = 0;
                  this.StationList[n].skip_scan = 1;
              } else {
                  this.StationList[n].in_range = 1;
                  this.StationList[n].skip_scan = 0;
              }

              output_html += this.StationList[n].gen_html();

          }
    
          output_html += "</table>";
    
          return output_html;
      }

      obj.redraw_column = function(response) {
          var Right = document.getElementById(this.Column);
          Right.innerHTML = response;
          var arr = Right.getElementsByTagName('script')
          for (var n = 0; n < arr.length; n++)
              eval(arr[n].innerHTML);
          Right.innerHTML = this.fill_column(this.StationList); 
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
          return "<th class='text-centered'>" + this.Name + "</th>";
      };

      obj.add_row = function() {
          return "<td id=\"Col " + name + "\" valign='top'></td>";
      };

      obj.add_station = function (station) {
           station.parent_index = this.StationList.length;
           station.parent_array = "Column" + this.Num + "Object.StationList";
           this.StationList.push(station);
      };

      obj.sort_by_distance = function() {
          this.StationList.sort( function(a, b)  {
              if(a.Distance() < b.Distance()) { return -1 };
              if(a.Distance() > b.Distance()) { return  1 };

              return 0;
          });
 
          for(var n = 0; n < this.StationList.length; n++)
              this.StationList[n].parent_index = n;
      };

      titles.innerHTML += "<th class='text-centered'>" + obj.Name + "</th>";
      rows.innerHTML += "<td id=\"" + obj.Column + "\" valign='top'></td>";

      obj.fill_array(name, file, num, obj.StationList);

      return obj;
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
        this.StationList.push(station);
        this.redraw_column(" ");
        this.Scan();
    };

    Favorites.remove_station = function (station) {
        var arr = this.StationList;
        for(var n=0; n<arr.length; n++) 
            if(arr[n] == station) {
                 arr.splice(n, 1);
                 break;
            }
            
        this.redraw_column(" ");
    };

    Favorites.Scan = function() {
        var header = document.getElementById("Active Station");
        var elem = this.StationList[1];

        header.innerHTML = "<h2 align='center'>" + elem.ListName + "<h2>" +
           "<h1 align='center' >" + elem.Frequency + "/" + elem.Tone + "<h1>" +
           "<h3 align='center' >" + elem.CallSign+ "</h3>";   
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
