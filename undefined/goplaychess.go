package main

import "fmt"

type Chess struct {
    color string
    steps int
    move_shape []int
    chess_x int
    chess_y int
}

func main(){
    var Pawn Chess
        Pawn.color;
        Pawn.steps = 1
        Pawn.move_shape = []int{1, 0, 1, 0, 1, 0, 1}
        Pawn.chess_x = 0
        Pawn.chess_y = 0

    var Rook Chess
        Rook.color;
        Rook.steps = 8
        Rook.move_shape = []int{8, 0, 8, 0, 8, 0, 8}
        Rook.chess_x = 0
        Rook.chess_y = 0

    var Queen Chess
        Queen.color;
        Queen.steps = 8
        Queen.move_shape = []int{8, 8, 8, 8, 8, 8, 8}
        Queen.chess_x = 0
        Queen.chess_y = 0

    var Knight Chess
        Knight.color;
        Knight.steps = [2, 1]
        Knight.move_shape = []int{2, 0, 2, 0, 2, 0, 2}
        Knight.chess_x = 0
        Knight.chess_y = 0

/* Test if everything works.
    var i int
    for i = 0; i < len(Pawn.move_shape); i++{
        fmt.Printf("Number = %d\n", Pawn.move_shape[i])
    }
}
*/