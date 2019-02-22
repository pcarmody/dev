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
  <!-- Modal - rig control -->
  <div class="modal fade" id="exampleModal" tabindex="-1" role="dialog" aria-labelledby="exampleModalLabel" aria-hidden="true">
    <div class="modal-dialog" role="document">
      <div class="modal-content">
        <div class="modal-header">
          <h5 class="modal-title" id="exampleModalLabel">Rig Control</h5>
          <button type="button" class="close" data-dismiss="modal" aria-label="Close">
            <span aria-hidden="true">&times;</span>
          </button>
        </div>
        <div class="modal-body" id='modalbody'>
        </div>
        <div class="modal-footer">
          <button type="button" class="btn btn-secondary" data-dismiss="modal">Close</button>
          <button type="button" class="btn btn-primary">Save changes</button>
        </div>
      </div>
    </div>
  </div>
<!-- define the <div> sections that will be used later and mark them as 'hidden' -->
<div style="display:none">
        <div id="Rig Status">
          <h2 align="center">XXXListName</h2>
          <h1 align="center">XXXFrequency</h1>
          <h3 align="center">XXXCallSign -- XXXComment</h3>
          <p align="center">Mode: XXXMode Power: XXXPower CTCSS: XXXCTCSS</p>
          <p align="center">Lattitude: XXXLattitude Longitutde: XXXLongitude </p>
        </div>
        <div class="modal-body" id='mymodalbody'>
            <h2 align='center'>List Name<h2>
               <h1 align='center' onclick='toggle_scan();'> 
                <div class="row justify-content-md-center input-group input-group-lg">
                   <input type="number" class="form-control col-sm-4" id="exampleInputEmail1"  placeholder="164.200">/
                   <input type="text" class="form-control col-sm-2" id="exampleInputEmail1"  placeholder="89.0">
                </div>
               </h1>
               <h3 align='center' > AJ6HF -- Me, Myself and I</h3>   
                <div class="row justify-content-md-center">
                 <div class="btn-group btn-group-toggle" data-toggle="buttons">
                   <label class="btn btn-secondary active">
                     <input type="radio" name="options" id="option1" autocomplete="off" checked>Contact
                   </label>
                   <label class="btn btn-secondary">
                     <input type="radio" name="options" id="option2" autocomplete="off">Station
                   </label>
                   <label class="btn btn-secondary">
                     <input type="radio" name="options" id="option3" autocomplete="off">Repeater
                   </label>
                 </div>
                </div>
                <div class="row justify-content-md-center">
                   <div class="col-xs-2">
                     Mode:
                    <select class="form-control input-small" id="sel1">
                      <option>LSB</option>
                      <option>USB</option>
                      <option>CW-U</option>
                      <option>FM</option>
                      <option>AM</option>
                      <option>RTTY-LSB</option>
                      <option>CW-L</option>
                      <option>DATA-LSB</option>
                      <option>RTTY-USB</option>
                      <option>DATA-FM</option>
                      <option>FM-N</option>
                      <option>DATA-USB</option>
                      <option>AM-N</option>
                      <option>C4FM</option>
                    </select>
                   </div>
                   <div class="col-xs-2">
                     Power:
                    <select class="form-control input-small" id="sel1">
                      <option>10</option>
                      <option>50</option>
                      <option>100</option>
                    </select>
                   </div>
                   <div class="col-xs-2">
                     CTCSS:
                    <select class="form-control input-small" id="sel1">
                     <option>67.0</option>
                     <option>69.3</option>
                     <option>71.9</option>
                     <option>74.4</option>
                     <option>77.0</option>
                     <option>79.7</option>
                     <option>82.5</option>
                     <option>85.4</option>
                     <option>88.5</option>
                     <option>91.5</option>
                     <option>94.8</option>
                     <option>97.4</option>
                     <option>100.0</option>
                     <option>103.5</option>
                     <option>107.2</option>
                     <option>110.9</option>
                     <option>114.8</option>
                     <option>118.8</option>
                     <option>123.0</option>
                     <option>127.3</option>
                     <option>131.8</option>
                     <option>136.5</option>
                     <option>141.3</option>
                     <option>146.2</option>
                     <option>151.4</option>
                     <option>156.7</option>
                     <option>159.8</option>
                     <option>162.2</option>
                     <option>165.5</option>
                     <option>167.9</option>
                     <option>171.3</option>
                     <option>173.8</option>
                     <option>177.3</option>
                     <option>179.9</option>
                     <option>183.5</option>
                     <option>186.2</option>
                     <option>189.9</option>
                     <option>192.8</option>
                     <option>196.6</option>
                     <option>199.5</option>
                     <option>203.5</option>
                     <option>206.5</option>
                     <option>210.7</option>
                     <option>218.1</option>
                     <option>225.7</option>
                     <option>229.1</option>
                     <option>233.6</option>
                     <option>241.8</option>
                     <option>25.3</option>
                     <option>254.1</option>
                    </select>
                   </div>
                </div>
                <div class="row justify-content-md-center">
                <div class="row justify-content-md-center input-group input-group-lg">
                   Lattitude
                   <input type="number" class="form-control col-sm-3" id="exampleInputEmail1"  placeholder="164.200">
                   Longitude
                   <input type="number" class="form-control col-sm-3" id="exampleInputEmail1"  placeholder="89.0">
                </div>
                </div>
          ...
        </div>
  <div id='superfluous'>
    <div class="form-check">
      <input class="form-check-input" type="checkbox" value="" id="ColumnScanNNN">
      <label class="form-check-label" for="ColumnScanNNN">
        Default checkbox
      </label>
    </div>
    <div class="form-check">
      <input class="form-check-input" type="checkbox" value="" id="defaultCheck2" disabled>
      <label class="form-check-label" for="defaultCheck2">
        Disabled checkbox
      </label>
    </div>
  </div>
  <div id='ColumnForm'>
    <form>
      <div class="form-group">
        <label for="ColumnNameNNN">Name</label>
        <input type="text" class="form-control" id="ColumnNameNNN" value="mydata" onchange="ColumnNNNObject.update_data(this.value);">
      </div>
      <div class="form-group">
        <label for="formGroupExampleInput2">Another label</label>
        <input type="text" class="form-control" id="formGroupExampleInput2" placeholder="Another input">
      </div>
    </form>
  </div>
</div>


<nav class="navbar navbar-expand-lg navbar-light bg-light">
  <a class="navbar-brand" href="#">Navbar</a>
  <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
    <span class="navbar-toggler-icon"></span>
  </button>

  <div class="collapse navbar-collapse" id="navbarSupportedContent">
    <ul class="navbar-nav mr-auto">
      <li class="nav-item active">
        <a class="nav-link" href="#">Home <span class="sr-only">(current)</span></a>
      </li>
      <li class="nav-item">
        <a class="nav-link" href="#">Link</a>
      </li>
      <li class="nav-item dropdown">
        <a class="nav-link dropdown-toggle" href="#" id="navbarDropdown" role="button" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Dropdown
        </a>
        <div class="dropdown-menu" aria-labelledby="navbarDropdown">
          <a class="dropdown-item" href="#stuff">Action</a>
          <a class="dropdown-item" href="/nonsense">Another action</a>
          <div class="dropdown-divider"></div>
          <a class="dropdown-item" href="#">Something else here</a>
        </div>
      </li>
      <li class="nav-item">
        <a class="nav-link disabled" href="#">Disabled</a>
      </li>
    </ul>
    <button type="button" class="btn btn-primary" data-toggle="modal" data-target="#exampleModal" onclick="get_insertmymodal();">
      Rig
    </button>
    <form class="form-inline my-2 my-lg-0">
      <input class="form-control mr-sm-2" type="search" placeholder="Search" aria-label="Search">
      <button class="btn btn-outline-success my-2 my-sm-0" type="submit">Search</button>
    </form>
  </div>
</nav>

  <div id="mapdiv" style="width: 30%; float: left;">
      <div id="popup" class="ol-popup">
          <a href="#" id="popup-closer" class="ol-popup-closer"></a>
          <div id="popup-content"></div>
      </div>
  </div>
<h1 id='Active Station' align="center">
   <br>Waiting...<br>
</h1>
<style>
    #table-wrapper {
      position:relative;
      height:50%;
    }
    #table-scroll {
      height:100%;
      overflow:auto;  
      margin-top:20px;
    }
    #table-wrapper table {
      width:100%;
    
    }
    #table-wrapper table * {
      background:white;
      color:black;
    }
    #table-wrapper table thead th .text {
      position:absolute;   
      top:-20px;
      z-index:2;
      height:20px;
      width:35%;
      border:1px solid red;
    }
</style>
<div id="table-wrapper">
  <div id="table-scroll">
    <table>
    <tbody>
    <tr id="TitleRow0"> </tr>
    <tr id="DataRow0"> </tr>
    </tbody>
    </table>
  </div>
</div>
<div id="table-wrapper">
  <div id="table-scroll">
    <table>
    <tbody>
    <tr id="TitleRow1"> </tr>
    <tr id="DataRow1"> </tr>
    </tbody>
    </table>
  </div>
</div>
<div id="BottomDiv" style="clear: both;">Below</div>
  <script src="http://www.openlayers.org/api/OpenLayers.js"></script>
  <script>
    function retrieve_rig_info(rig_info_num, count) {
              var xhttp2= new XMLHttpRequest();
              xhttp2.onreadystatechange = function() {
                if (this.readyState == 4 && this.status == 200) {
                    rig_info = JSON.parse(this.responseText);
                    if(rig_info == 'waiting') 
                        if(count > 9)
                            alert("Rig not responding");
                        else
                            setTimeout(function() { retrieve_rig_info(rig_info_num, count+1); }, 700)
                    else
                        insertmymodal(rig_info);
                };
              };
              cmd = Config.NodeServer+"?result="+rig_info_num;
              xhttp2.open("GET", cmd, true);
              xhttp2.send();
    };

    function get_insertmymodal() {
        var xhttp = new XMLHttpRequest();
        var rig_info_num = 0; 
        var rig_info = "";

        xhttp.onreadystatechange = function() {
          if (this.readyState == 4 && this.status == 200) {
              rig_info_num = this.responseText;
//alert("retrieved rig_info_num = "+rig_info_num);
              retrieve_rig_info(rig_info_num, 0);
          };
        };
        cmd = Config.NodeServer+"?get_rig_info=1";
        xhttp.open("GET", cmd, true);
        xhttp.send();

i//        setTimeout(insertmymodal, 700)
    };

    function insertmymodal(rig_info) {
//        var mymodal = document.getElementById('mymodalbody');
        var mymodal = document.getElementById('Rig Status');
        var modal = document.getElementById('modalbody');
        modal.innerHTML = mymodal.innerHTML. //"<h1>my header</h1>";
            replace(/XXXListName/g,"Favorites").
            replace(/XXXFrequency/g,"7.200 MHz").
            replace(/XXXMode/g, "FM").
            replace(/XXXComment/g,"Yours, Mine and Hours").
            replace(/XXXPower/g,"50 watts").
            replace(/XXXLattitude/g,"Lat").
            replace(/XXXLongitude/g,"Lon").
            replace(/XXXCTCSS/g,"69.7").
            replace(/XXXCallSign/g,"AJ6HF");
    };

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

    function ConfigObject() {
        var config = new Object();

        config.Range = 40;
        config.NodeServer = "http://127.0.0.1:8080/";
        config.Rigctl_TCPIP_address = "127.0.0.1";
        config.Rigctl_TCPIP_port = "4543";

        config.stringify = function () {

          var txt = "{";
  
          txt += '"Range":' + config.Range;
          txt += ', ';

          txt += '"NodeServer":"' + config.NodeServer + '"';
          txt += ', ';
  
          txt += '"Rigctl_TcPIP_address":"' + config.Rigctl_TcPIP_address + '"';
          txt += ', ';
  
          txt += '"Rigctl_TCPIP_port":"' + config.Rigctl_TCPIP_port + '"';
          txt += '};';

          return txt;
        };

        return config;
    };

var Config = ConfigObject();

var Geographic  = new OpenLayers.Projection("EPSG:4326"); 
var Mercator = new OpenLayers.Projection("EPSG:900913");

    function StationObject(markers, call_sign, freq, tone, comment, icon, lon, lat, column_object) {
        var obj = new Object();
        obj.CallSign = call_sign;
        obj.Frequency = freq;
        obj.Tone = tone;
        obj.Comment = comment;
        obj.Icon = icon;
        obj.Lon = lon;
        obj.Lat = lat;
        obj.ListName = column_object.Name;
        obj.Column = column_object;

        obj.stringify = function() {
            var txt = '{';
  
          txt += '"CallSign":"' + obj.CallSign + '"';
          txt += ', ';
  
          txt += '"Frequency":"' + obj.Frequency + '"';
          txt += ', ';
  
          txt += '"Tone":"' + obj.Tone + '"';
          txt += ', ';
  
          txt += '"Comment":"' + obj.Comment + '"';
          txt += ', ';
  
          txt += '"Icon":"' + obj.Icon + '"';
          txt += ', ';
  
          txt += '"Lon":"' + obj.Lon + '"';
          txt += ', ';
  
          txt += '"Lat":"' + obj.Lat + '"';
          txt += ', ';
  
          txt += '"ListName":"' + obj.ListName + '"';
          txt += '} ';

          return txt;
        };

        obj.in_range = function() {
            if(obj.Range)
                return obj.Range;

            return obj.Column.get_range();
        };

        obj.set_scan_flags = function() {
if(debug) return;

              if(obj.Distance() > obj.in_range()) {
                  obj.in_range = 0;
                  obj.skip_scan = 1;
              } else {
                  obj.in_range = 1;
                  obj.skip_scan = 0;
              }

        };

        obj.CanScan = function() {
            return obj.in_range && !obj.skip_scan;
        };

        obj.get_results = function(header) {
     
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
              if (this.readyState == 4 && this.status == 200) {
                  obj.rig_response = this.responseText;
                  header.innerHTML = obj.gen_header();
              };
            };
            cmd = Config.NodeServer+"?result="+obj.rig_result;
            xhttp.open("GET", cmd, true);
            xhttp.send();
        };

        obj.set_freq = function(header) {
     
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
              if (this.readyState == 4 && this.status == 200) {
//              if (this.readyState == 4) {
                  obj.rig_result = this.responseText;
//                  setTimeout(obj.get_results, 700)
                  obj.get_results(header);
              };
            };
            var frequency = parseFloat(this.Frequency).toFixed(3);
            cmd = Config.NodeServer+"?set_freq="+ frequency + "&set_ctcss_tone="+this.Tone;
            xhttp.open("GET", cmd, true);
            xhttp.send();
        };

        obj.get_strength = function() {
// 
//  call the rig server to ask for informaiton
//    
            var xhttp = new XMLHttpRequest();
            xhttp.onreadystatechange = function() {
              if (this.readyState == 4 && this.status == 200) {
//
//  call the rig server again to get the result
//
                    var xhttp2 = new XMLHttpRequest();
                    xhttp2.onreadystatechange = function() {
                      if (this.readyState == 4 && this.status == 200) {
                          obj.rig_result = this.responseText;
                          alert("signal strength is" + obj.rig_result);
                      };
                    };
                    cmd = Config.NodeServer+"?result="+obj.rig_result;
                    xhttp2.open("GET", cmd, true);
                    xhttp2.send();
                  obj.rig_result = this.responseText;
              };
            };
            cmd = Config.NodeServer+"?get_strength=1";
            xhttp.open("GET", cmd, true);
            xhttp.send();

        }
    
        var GPSlon = -122.365530;
        var GPSlat = 37.251690; 

        obj.Distance = function() {
//
// two lat and lon and returns the distance between them as the crow flies (in km)
//
            var point1 = new OpenLayers.Geometry.Point(this.Lon, this.Lat).transform(Geographic, Mercator);
            var point2 = new OpenLayers.Geometry.Point(GPSlon, GPSlat).transform(Geographic, Mercator);       
            retval = point1.distanceTo(point2) * 0.61 / 1000.0;
            return retval;
        };

        obj.array_string = function() {
           return this.parent_array + "[" + this.parent_index + "]";
        };

        obj.toggle_skip = function() {

            this.skip_scan = (this.skip_scan)? 0 : 1;

        };

        obj.gen_icon = function() {
            return "<img src='" + this.Icon + "'> ";
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
//            var on_click = this.array_string()+".set_freq();" + this.array_string()+".get_strength();";
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
             
            return "<tr><td><div class='dropdown'>" +
              "  <button type='button' class='btn " + button_type + "' data-toggle='dropdown'>" +
              this.gen_icon() + this.CallSign +
              "  </button>" +
              "  <div class='dropdown-menu'>" +
              "    <h3>"+this.ListName+"</h3>" +
                   call_sign_button + skip_button + " " + map_button + "<br>" +
                   this.Frequency + "/" + this.Tone + "<br>" + 
                   "<div class='font-weight-bold'>" + this.Comment + "</div><br>"  +
                this.Distance().toFixed(2) + " miles"; + 
              "  </div>" +
              "</div></td></tr>";
        };

        obj.gen_header = function() {

            var background_color = '';
            if(ScanInterval == 0) 
                background_color = ' style="background-color:rgb(255, 0, 0);"';
            var value =  this.gen_icon() + this.Frequency + "/" + this.Tone ;

            return "<h2 align='center'>" + this.ListName + "<h2>" +
               "<h1 align='center' onclick='toggle_scan();'" + background_color + ">" + 
                   value + 
               "</h1>" +
               "<h3 align='center' >" + this.CallSign+ " -- " + this.Comment + "-- " + this.rig_response + "</h3>";   
        };

        obj.gen_popup = function() {
            return "<h2>" + this.ListName + "</h2>" + 
                   "<h3>" + this.CallSign + "</h3>" +  
                   this.Frequency + "/" + this.Tone + "<br>" + 
                   "<bold>" + this.Comment + "</bold><br>" +
                this.Distance().toFixed(2) + " miles"; 
        };

        if(markers)
            add_freq_marker(markers, obj);

        return obj;
    };

//
// column object definition
//
var debug = 0;

    function ColumnObject(name, file, num, titles_name, rows_name, icon, link) {
      var titles = document.getElementById(titles_name);
      var rows = document.getElementById(rows_name);

      var obj = new Object();

      obj.StationList = new Array();
      obj.Name = name;
      obj.File = file;
      obj.Num = num;
      obj.Column = "Col " + name;
      obj.Icon = icon;
      obj.Link = link;
      obj.skip_scan = 1;
      obj.scan_index = 0;

      obj.stringify = function() {

          var txt = "{"
  
          txt += '"Name":"' + obj.Name + '"';
          txt += ', ';
  
          txt += '"Num":' + obj.Num;
          txt += ', ';
  
          txt += '"File":"' + obj.File + '"';
          txt += ', ';
  
          txt += '"Column":"' + obj.Column + '"';
          txt += ', ';
  
          txt += '"Icon":"' + obj.Icon + '"';
          txt += ', ';
  
          txt += '"Range":' + obj.Range;
          txt += ', ';
  
          txt += '"StationList" : [';
          for(var i=0; i<obj.StationList.length; i++)
              txt += this.StationList[i].stringify() + ',';
          txt += '""]';
          txt += '} ';

          return txt;
      };

      obj.load = function(storage) {
          obj.Name = storage.Name;
          obj.Num = storage.Num;
          obj.File = storage.File;
          obj.Column = storage.Column;
          obj.Icon = storage.Icon;
          obj.Link = storage.Link;
          obj.Range = storage.Range;
          obj.StationList = new Array();

          for(var i=0; i<storage.StationList.length; i++) {
              var stat = storage.StationList[i];
              if(!stat.CallSign)
                  break;
              var station = StationObject(0, stat.CallSign, stat.Frequency, stat.Tone, stat.Comment, stat.Icon, stat.Lon, stat.Lat, Favorites);
//              var station = StationObject(0, stat.CallSign, stat.Frequency, stat.Tone, stat.Comment, stat.Icon, stat.Lon, stat.Lat, stat.ListName);
              obj.StationList.push(station);
          }
          obj.redraw_column(' ');
      };

      obj.fill_column = function() {
          var output_html = "<table>";
          for (var n = 0; n < this.StationList.length; n++) {

              this.StationList[n].set_scan_flags();

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
//          Right.innerHTML = this.fill_column(this.StationList); 
          Right.innerHTML = this.fill_column(); 
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

      obj.update_title = function() {
          var header_id = obj.Name + "_header";
          var header = document.getElementById(header_id);
          header.innerHTML = obj.add_title();
      };

      obj.update_data = function(evnt) {

              alert("changed in "+obj.Name+":"+evnt);
      };
    
      obj.add_title = function() {
          var header_id = obj.Name + "_header";
          var button_type = "btn-light ";
          var link = "";
          var object_name = "Column"+obj.Num+"Object";
          var column_name = document.getElementById('ColumnNameNNN');
          column_name.value = obj.Name;
          var ColumnForm = document.getElementById("ColumnForm").innerHTML.replace(/NNN/g, obj.Num).replace(/mydata/, obj.Name);
          

          var skip_button = "<a class='btn-light' href='javascript: " + object_name + ".toggle_skip();'>";
          if(obj.CanScan())
              skip_button += 'skip';
          else {
              button_type += "font-italic text-info";
              skip_button += "scan";
          }
          skip_button += "</a>";  

          if(obj.Link)
              link = '<a href="' + obj.Link + '">website</a>';
//          return "<th id='" + header_id + "' class='text-centered' onclick='alert(\"clicked\");'>" + obj.gen_icon() + obj.Name + "</th>";
          return "<th id= '" + header_id + "' class='text-centered'>" + 
            "<div class='dropdown'>" +
            "  <button type='button' class='btn " + button_type + "' data-toggle='dropdown'>" +
            obj.gen_icon() + obj.Name +
            "  </button>" +
            "  <div class='dropdown-menu'>" +
            "    <h3>"+obj.Name+"</h3>" +
                 link + " " + skip_button + "<hr>" + ColumnForm +
            "  </div>" +
            "</div></th>";
      };

      obj.gen_icon = function() {
          return "<img src='http://127.0.0.1/repeatermap/icons/" + this.Icon + "'>";
      };

      obj.add_row = function() {
          return "<td id=\"" + obj.Column + "\" valign='top'></td>";
      };

      obj.add_station = function (station) {
           station.parent_index = this.StationList.length;
           station.parent_array = "Column" + this.Num + "Object.StationList";
           station.MapIcon = this.Icon;
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

      obj.toggle_skip = function() {
          obj.skip_scan = (obj.skip_scan)? 0 : 1;
          obj.update_title();
//          obj.skip_scan = !obj.skip_scan;
      };
          

      obj.CanScan = function() {
          return !obj.skip_scan;
      };

      obj.Scan = function(index) {
          var header = document.getElementById("Active Station");
          var elem = this.StationList[index];
          elem.set_freq(header);
//          header.innerHTML = elem.gen_header();
      };

      obj.Scan_Next = function() {

          if(!obj.CanScan()) 
              return 0; 

          if(obj.StationList.length == 0)
              return 0;

          if(obj.scan_index >= obj.StationList.length) 
              obj.scan_index = 0;

          var elem = '';
          do {
              elem = obj.StationList[obj.scan_index++];
          } while (!elem.CanScan() && obj.scan_index < obj.StationList.length);

          if(obj.scan_index > obj.StationList.length) {
              return 0;
          }

          var header = document.getElementById("Active Station");
          elem.set_freq(header);
//          header.innerHTML = elem.gen_header();
          CurrentStation = elem;

          return 1;
      };

      obj.get_range = function() {

          if(obj.Range)
              return obj.Range;

          return Config.Range;
      };

      titles.innerHTML += obj.add_title();
//      rows.innerHTML += "<td id=\"" + obj.Column + "\" valign='top'></td>";
      rows.innerHTML += obj.add_row();

      obj.fill_array(name, file, num, obj.StationList);

      return obj;
    };

/*
    notes from HamLib

int tone_list [] = { 670,693,719,744,77,797,825,854,885,915,948,974,1000,1035,1072,11009,1148,1188,1230,1273,1318,1365,1413,1462,1514,1567,1598,1622,1655,1679,1713,1738,1773,1799,1835,1862,1899,1928,1966,1995,2035,2065,2107,2181,2257,2291,2336,2418,253,2541 };

// P2 MODE 1: LSB 2: USB 3: CW-U 4: FM 5: AM 6: RTTY-LSB 7: CW-L 8: DATA-LSB 9: RTTY-USB A: DATA-FM B: FM-N C: DATA-USB D: AM-N E: C4FM
char *modes [] = { "", "LSB", "USB", "CW-U", "FM", "AM", "RTTY-LSB", "CW-L", "DATA-LSB", "RTTY-USB", "DATA-FM", "FM-N", "DATA-USB", "AM-N", "C4FM" }; */

    var titles = document.getElementById("TitleRow0");
    var datarow = document.getElementById("DataRow0");
    var titles_name = "TitleRow0";
    var datarow_name = "DataRow0";
    var ColumnObjects = new Array();
    var CurrentStation = 0;
//    var Favorites = ColumnObject("Favorites", " ", 1, titles, datarow);
    var Favorites = ColumnObject("Favorites", " ", 1, titles_name, datarow_name);
    ColumnObjects.push(Favorites);

//
// redefine add_station for Favorites
//

    function load_favorites() {
        var xhttp = new XMLHttpRequest();
        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                var storage = JSON.parse(this.responseText);
                Favorites.load(storage);
            };
          }; 
        xhttp.open("GET", Config.NodeServer+"?load=1", true);
        xhttp.send();
    };

    save_favorites = function() {
        var xhttp = new XMLHttpRequest();
/*        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                alert("qqq " + this.responseText);
            };
          }; */
        xhttp.open("GET", Config.NodeServer+"?save="+Favorites.stringify(), true);
        xhttp.send();
    };

    function save_config() {
        var xhttp = new XMLHttpRequest();
/*        xhttp.onreadystatechange = function() {
            if (this.readyState == 4 && this.status == 200) {
                alert("qqq " + this.responseText);
            };
          }; */
        xhttp.open("GET", Config.NodeServer+"?save_config="+Config.stringify(), true);
        xhttp.send();
    };

    Favorites.toggle_skip();
//    Favorites.CanScan = function() {
//        return 1;
//    };

    Favorites.add_station = function (station) {
debug = 1;
        this.StationList.push(station);
        this.redraw_column(" ");
        save_favorites();
    };

    Favorites.remove_station = function (station) {
        var arr = this.StationList;
        for(var n=0; n<arr.length; n++) 
            if(arr[n] == station) {
                 arr.splice(n, 1);
                 break;
            }
            
        this.redraw_column(" ");
        this.save();
    };

//
//  global functions -- iterate through the columns
//
    var scan_index = 0;

    function scan_favorites() {
        if(Favorites.StationList.length == 0)
            return 0;
        if(scan_index >= Favorites.StationList.length)
            scan_index = 0;
        return Favorites.Scan(scan_index++);
    };

    function scan_all() {
        if(ColumnObjects.length == 0)
            return 0;
        if(scan_index > ColumnObjects.length)
            scan_index = 0;

        while(scan_index < ColumnObjects.length)
            if(ColumnObjects[scan_index].Scan_Next()) 
                return;
            else
                scan_index++;
    };

<?php
    $list = `ls StationLists`;
    $file_names = str_getcsv($list, "\n");
#    echo $file_names[0];
    $f = fopen("StationLists/lists.csv", "r");
    $arrays = "";
    $i = 0;
    $row = 0;
    $titles_name = "TitleRow".$row;
    $datarow_name = "DataRow".$row;
    while (($line = fgetcsv($f)) !== false) {
        $i = $i + 1;
        if($i == 1) {
            continue;
        }
        if($i == 6) {
            $row = $row + 1;
            $titles_name = "TitleRow".$row;
            $datarow_name = "DataRow".$row;
#            break;
        }
        $new_obj = "Column".$i."Object ";
#        $arrays = $arrays ."    var ".$new_obj." = ColumnObject(\"".$line[0]."\", \"".$line[1]."\", ".$i.", titles, datarow, '" . $line[3] . "');\n";
        $parm1 = '"'.$line[0].'"';
        $parm2 = '"'.$line[1].'"';
        $parm3 = $i;
        $parm4 = '"'.$titles_name.'"';
        $parm5 = '"'.$datarow_name.'"';
        $parm6 = '"'.$line[3].'"';
        $parm7 = '"'.$line[4].'"';
        $arrays = $arrays ."    var ".$new_obj." = ColumnObject(".$parm1.','.$parm2.','.$parm3.','.$parm4.','.$parm5.','.$parm6.','.$parm7.");\n";
        $arrays = $arrays ."    ColumnObjects.push(".$new_obj.");\n";
    }
    echo $arrays;
?>

    var ScanInterval = 0;
    function start_scan() {
        ScanInterval = setInterval(scan_all, 3000);
    };

    function stop_scan() {
        clearInterval(ScanInterval);
    };

    function toggle_scan() {
        if(ScanInterval) {
            clearInterval(ScanInterval);
            ScanInterval = 0;
        } else
            ScanInterval = setInterval(scan_all, 3000);
        var header = document.getElementById("Active Station");
        header.innerHTML = CurrentStation.gen_header();
    };

    load_favorites();
    toggle_scan();
//    var MyVar = setInterval(scan_favorites, 3000);
</script>
</body></html>
