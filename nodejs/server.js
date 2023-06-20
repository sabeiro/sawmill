// https://www.interviewbit.com/blog/node-js-projects/
var express = require("express");
var app = express();
var port = process.env.PORT || 5013;
const https = require('https');
const fs = require('fs');
const certs = {
  key: fs.readFileSync('localhost-key.pem'),
  cert: fs.readFileSync('localhost.pem'),
};

app.set('views', __dirname + '/views');
app.set('view engine', "jade");
app.engine('jade', require('jade').__express);
app.get("/", function(req, res){
    res.render("page");
});

app.use(express.static(__dirname + '/public'));
// var midPort = app.listen(port, function (){console.log('Node.js listening on port ' + port);})
var httpsServer = https.createServer(certs, app);
httpsServer.listen(port);
var io = require('socket.io').listen(httpsServer);

io.sockets.on('connection', function (socket) {
    socket.emit('message', { message: 'Welcome to the Real Time Web Chat' });
    socket.on('send', function (data) {
        io.sockets.emit('message', data);
    });
});
