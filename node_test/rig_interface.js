var http = require('http');
var url = require('url');
var net = require('net');
var responses = new Array(100);

var send_rig_command = function (num, cmd) {
    var client = new net.Socket();

    client.connect(4543, '127.0.0.1', function() {
    	console.log('Connected '+cmd);
    	client.write(cmd+'\n');
    });
    
    client.on('data', function(data) {
    	console.log('Received: ' + data);
        responses[num] = data;
    	client.destroy(); // kill client after server's response
    });
    
    client.on('close', function() {
    	console.log('Connection closed');
    });

    return num;
};

var set_freq = function(num, query) {
     send_rig_command(num, 'F'+query.set_freq);
     return num;
};

var get_freq = function(num, query) {
    send_rig_command(num, 'f');
    return num;
};

var query_num = 0;

http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/html'});
  var q = url.parse(req.url, true).query;
  var txt = '';

  console.log(q);

  query_num += 1;
  responses[query_num] = "waiting";

  if(q.result) {
      txt = responses[q.result];
  }

  if(q.set_freq) {
      txt += set_freq(query_num, q);
  } 

  if (q.get_freq) {
      txt += get_freq(query_num, q);
  }

  res.end(txt);
}).listen(8080);


