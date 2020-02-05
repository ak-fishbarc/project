package src

import "database/sql"
import _ "github.com/lib/pq"
import "fmt"
/* Test func
func insert_data(args[]string){
    Zero = 1
}
*/

func Connect() (string){
    db, err := sql.Open("postgres", "user=postgres dbname=Chess sslmode=disable")
    if err != nil{
        fmt.Printf("Error: %q", err)
    }
    rows := db.QueryRow("INSERT INTO pieces(name, color) VALUES('knight', 'white') RETURNING name")

    return fmt.Sprintf("Query successful: %q", rows)
}