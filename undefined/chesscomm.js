var http = require('http');
var cb = require('./chessboard.js');
var events = require('events');
var eventEmitter = new events.EventEmitter();
var eventHandler = function(){
       cb.show_board();
};

http.createServer(function (req, res){
    res.writeHead(200, {'Content-type': 'text/plain'});
    eventEmitter.on('show_board', eventHandler);
    eventEmitter.emit('show_board');
    res.end();
}).listen(8333);