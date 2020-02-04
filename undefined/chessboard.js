var Chessboard = {
    width:8,
    height:8,
    board:0,
    set chessboard(b){
    	this.board = b;
    }
};

var new_board = createBoard(Chessboard.height, Chessboard.width);
Chessboard.chessboard = new_board;

function createBoard(x, y){
    var board = [];
    for(i = 0; i < x; i++){
        board[i] = []
        for(j = 0; j < y; j++){
            board[i].push([j])
            };
    };
    return board;
}

exports.show_board = function(){
    console.log(Chessboard.board);
};