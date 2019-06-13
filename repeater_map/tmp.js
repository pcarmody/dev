
var net = require('net');
var http = require('http');
var url = require('url');

http.createServer(function (req, res) {
  res.writeHead(200, {'Content-Type': 'text/html', "Access-Control-Allow-Origin": "*" });
  var q = url.parse(req.url, true).query;
console.log(q);
     res.end('<html><body>Hello World!</body/</html>');
}).listen(8080);
/*net.createServer(function (socket) {
    socket.write("garbage in garbage out");
    socket.pipe(socket);
}).listen(8080);*/
