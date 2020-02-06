package main

import (
    "fmt"
    "time"
    "./src"
)
var parts [4] string
var i = 0

func createPart(part string){
    fmt.Println(part, " was manufactured")
    parts[i] = part
    i++
}

func packAndSend(partsToPack [4]string){
    var body int
    var arms int
    var legs int
    var head int
    for i=0; i < len(partsToPack); i++{
        fmt.Println("Part " + partsToPack[i] + " is ready for packing!")
        parts[i] = ""
        switch{
        case partsToPack[i] == "Body":
            body = 1
        case partsToPack[i] == "Arms":
            arms = 1
        case partsToPack[i] == "Legs":
            legs = 1
        case partsToPack[i] == "Head":
            head = 1
        }
        time.Sleep(1 * time.Second)
        }

    if (body == 0 || arms == 0 || legs == 0 || head == 0){
        fmt.Println("Missing parts ! Abort !")
    }else{
        fmt.Println("Organizing parts.")
        time.Sleep(1 * time.Second)
        partsToPack[0] = "'Body'"
        partsToPack[1] = "'Head'"
        partsToPack[2] = "'Arms'"
        partsToPack[3] = "'Legs'"
        time.Sleep(1 * time.Second)
        var packedParts = []string{partsToPack[0], partsToPack[1], partsToPack[2], partsToPack[3]}
        for i = 0; i < len(packedParts); i++{
            fmt.Println("Sending " + packedParts[i] + " to the database!")
        }
        var columns = []string{"body", "head", "arms", "legs"}
        fmt.Println(src.Connect("robot", "parts", columns, packedParts))
    }
}

func main(){
    go createPart("Body")
    go createPart("Head")
    go createPart("Arms")
    go createPart("Legs")
    time.Sleep(5 * time.Second)
    /*
    for i=0; i < len(parts); i++{
        fmt.Println(parts[i])
        }
    */
    packAndSend(parts)
    time.Sleep(1 * time.Second)
    if (i == 3){
        i = 0
    }
}