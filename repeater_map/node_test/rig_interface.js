var http = require('http');
var url = require('url');
var net = require('net');
var fs = require('fs');

var responses = new Array(100);
var rig_status = { };
var status_update_rate = 15000;

var send_rig_command = function (num, cmd) {
    var client = new net.Socket();
    responses.push(" ");

    client.connect(4543, '127.0.0.1', function() {
    	console.log('Connected '+num+':'+cmd);
    	client.write(cmd+'\n');
    });
    
    client.on('data', function(data) {
    	console.log('Received: ' + num +':' + data);
        data = '' + data;
        num = parseInt(num);
        if(num < 10) {
            if(num == 0)
                rig_status.frequency = parseInt(data);
            else if(num == 1)
                rig_status.mode = data;
            else if(num == 2)
                rig_status.ctcss_tone = parseInt(data);
            else if(num == 3) 
                rig_status.power = parseInt(data.substring(3, 5));
            else if(num == 4)
                rig_status.s_meter = parseInt(data.substring(4,6));

            num = (num + 1) %5;
//            setTimeout(function() { cycle_rig_status(num+1);}, 1000);
        } else
            responses[num] = data;

        console.log('rig_status: '+JSON.stringify(rig_status));
    	client.destroy(); // kill client after server's response
    });
    
    client.on('close', function() {
    	console.log('Connection closed');
    });

    return num;
};

//
// these two tables are retrieved from ft_991a_cat_operating-manual.pdf
//

var ctcss_tone_list = [ 670,693,719,744,77,797,825,854,885,915,948,974,1000,1035,1072,11009,1148,1188,1230,1273,1318,1365,1413,1462,1514,1567,1598,1622,1655,1679,1713,1738,1773,1799,1835,1862,1899,1928,1966,1995,2035,2065,2107,2181,2257,2291,2336,2418,253,2541 ];

var dcs_tone_list = [ 23, 25, 26, 31, 32, 36, 43, 47, 51, 53, 54, 65, 71, 72, 73, 74, 114, 115, 116, 122, 125, 131, 132, 134, 143, 145, 152, 155, 156, 162, 165, 172, 174, 205, 212, 223, 225, 226, 243, 244, 245, 246, 251, 252, 255, 261, 263, 265, 266, 271, 274, 306, 311, 315, 325, 331, 332, 343, 346, 351, 356, 364, 365, 371, 411, 412, 413, 423, 431, 432, 445, 446, 452, 454, 455, 462, 464, 465, 466, 503, 506, 516, 523, 526, 532, 546, 565, 606, 612, 624, 627, 631, 632, 654, 662, 664, 703, 712, 723, 731, 732, 734, 743, 754];

var parse_rig_info = function(response) {
// IF001462125000+000010402000;CT02;CN00001;CN01000;PC050;SQ0005;SM0006;
/*
  IF : 0,1 ... 2 bytes
  memory : 3-5 ... 3 bytes
  frequence: 6-14       in hertz
  clarifier: 15-19      Clarifier Direction +: Plus Shift, --: Minus Shift Clarifier Offset: 0000 - 9999 (Hz)
  rx_clarifier_on: 20
  tx_clarifier_on: 21
  mode = 22             1: LSB 2: USB 3: CW 4: FM 5: AM 6: RTTY-LSB 7: CW-R 8: DATA-LSB 9: RTTY-USB A: DATA-FM B: FM-N C: DATA-USB  D: AM-N E: C4FM
  memory_bank = 23      0: VFO 1: Memory 2: Memory Tune 3: Quick Memory Bank (QMB) 4: QMB-MT 5: PMS 6: HOME
  CTCSS = 24            0: CTCSS “OFF” 1: CTCSS ENC/DEC 2: CTCSS ENC
  filler = '00'
  simplex_shift = 26    Simplex 1: Plus Shift 2: Minus Shift
  semi_colon = ';' 27
  CT code = 'CT0' 28-30
  ctcss_switch = 31     0: CTCSS “OFF” 1: CTCSS ENC/DEC “ON” 2: CTCSS ENC “ON” 3: DCS “ON” 
  semi_colon = ';' 32 
  CN CTCSS code 'CN00' = 33-36
  ctcss_code = 38-40
  semi_colon = ';' 41
  CN DCS code 'CN01' = 42-45
  dcs_code = 46-48
  semi_colon = ';' 49
  power code 'PC' = 50-51
  power level = 52-54
  semi_colon = ';' 55
  squelch cmd 'SQ0' = 56-58
  squelch = 59-61
  semi_colon = ';' 62
  s_meter cmd 'SM0' = 63-65
  s_meter = 66-68
  semi_colon = ';' 69
*/
    var frequency = response.substring(5,14);
    var clarifier = response.substring(15,19);
    var rx_clarifier = response[19];
    var tx_clarifier = response[20];
    var mode = parseInt(response[21]);
    var bank = response[22];
    var ctcss = response[23];
    var simplex_shift = response[26];
    var ctcss_switch = response[31];
    var ctcss_code = parseInt(response.substring(38, 40));
    var dcs_code = response.substring(46, 48);
    var power = parseInt(response.substring(52, 54));
    var squelch = parseInt(response.substring(59, 61));
    var s_meter = parseInt(response.substring(66, 68));
  
    var modes = [ " ", "LSB", "USB", "CW", "FM", "AM", "RTTY-LSB", "CW-R", "DATA-LSB", "RTTY-USB", "DATA-FM", "FM-N", "DATA-USB ", "AM-N", "C4FM"];

    rig_status = { "frequency": frequency, "clarifier": clarifier, "rx_clarifier": rx_clarifier, "tx_clarifier": tx_clarifier, "mode": modes[mode], "ctcss": ctcss, "simplex_shift": simplex_shift, "ctcss_switch": ctcss_switch, "ctcss_code": ctcss_tone_list[ctcss_code], "dcs_code": dcs_code, "power": power, "squelch": squelch, "s_meter": s_meter };

    console.log(rig_status);
    return JSON.stringify(rig_status);
};
 
var parse_rig_info2 = function(response) {

    if(response.indexOf('Frequency') !== -1) {
        var arr = response.match(/Frequency: (\d*);/)
        rig_status.frequency = arr[0];
    }
};

var set_ctcss_tone = function(query) {
     return 'C '+query.set_ctcss_tone.replace(/[^0-9a-z]/gi, '') + ';\n';
};

var set_freq = function(query) {
     return 'F '+query.set_freq.replace(/[^0-9a-z]/gi, '')+'000;\n';
};

var get_freq = function(query) {
    return 'f;';
};

var get_strength = function(query) {
    return 'SM0;';
};

var get_rig_info = function(query) {
    return 'w IF;CT0;CN00;CN01;PC;SQ0;SM0;';
};

var get_rig_info2 = function(query) {
    return 'fa;m;c;fa;d;r';
};

function cycle_rig_status(num) {
    
    var txt = 'w IF;';
    if(num == 0)
        txt = get_rig_info2(' ');
    else if(num == 1)
        txt = 'fa';
    else if(num == 2)
        txt = 'm';
    else if(num == 3)
        txt = 'c';
    else if(num == 4)
        txt = 'w PC;';
    else if(num == 5)
        txt = 'w SM0;';

    send_rig_command(num, txt);
};
//setInterval(function() { 
setTimeout(function() { cycle_rig_status(0);}, 1000);

var query_num = 10;

http.createServer(function (req, res) {

  var q = url.parse(req.url, true).query;
//
// if request for results return the results
//
  if(q.result) {
        var index = parseInt(q.result);
 
        if(!responses[index]) {
            res.writeHead(100, {'Content-Type': 'text/html', "Access-Control-Allow-Origin": "*" });
            res.end("waiting");
            return;
        }

        res.writeHead(200, {'Content-Type': 'text/html', "Access-Control-Allow-Origin": "*" });
        console.log('processing results '+q.result + ":" + responses[index]);
        res.end(responses[index]);
      return;
  }

  if(q.save) {
      fs.writeFile('favorites.json', q.save, (err) => {  
          // throws an error, you could also catch it here
          if (err) throw err;

          // success case, the file was saved
          console.log('Favorites saved!');
      });
      return;
  }

  if(q.save_config) {
      fs.writeFile('config.json', q.save_config, (err) => {  
          // throws an error, you could also catch it here
          if (err) throw err;

          // success case, the file was saved
          console.log('Configuration saved!');
      });
      return;
  }

  if(q.load) {
      console.log("loading favorites");
      res.writeHead(200, {'Content-Type': 'text/html', "Access-Control-Allow-Origin": "*" });
      fs.readFile('favorites.json', 'utf8', function(err, contents) {
          res.end(contents);
      });
      return;
  }

  if(q.get_rig_info) {
      console.log("retieving rig status");
      res.writeHead(200, {'Content-Type': 'text/html', "Access-Control-Allow-Origin": "*" });
      res.end(JSON.stringify(rig_status));
      return;
  }

  if(q.status_update_rate) {
      console.log("retieving rig status");
      res.writeHead(200, {'Content-Type': 'text/html', "Access-Control-Allow-Origin": "*" });
      if(q.status_update_rate == 0)
          res.end(status_update_rate);
      else
          res.end(q.status_update_rate);
      return;
  }

//
// otherwise continue
//

  res.writeHead(200, {'Content-Type': 'text/html', "Access-Control-Allow-Origin": "*" });
  var txt = '';

  console.log(q);

  query_num += 1;
  responses[query_num] = "waiting";

//
// otherwise construct rigctl command and deliver
//
  if(q.set_freq) {
      txt += set_freq(q);
  } 

  if (q.get_freq) {
      txt += get_freq(q);
  }

  if(q.set_ctcss_tone) {
      txt += set_ctcss_tone(q);
  } 

//  if(q.get_strength) {
//      txt += get_strength(q);
txt += "M FM 16000;";
//  }

  send_rig_command(query_num, txt);
  
//  send_rig_command(query_num, get_strength(q));

//  res.write(txt);
  res.end(query_num.toString());
  query_num++;
}).listen(8080);


