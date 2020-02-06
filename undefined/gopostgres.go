package src

import "database/sql"
import _ "github.com/lib/pq"
import "fmt"
import "strings"
/* Test func
func insert_data(args[]string){
    Zero = 1
}
*/

func Connect(dbname string, table string, columns []string, values []string) (string){
    db, err := sql.Open("postgres", "user=postgres dbname=" + dbname + " sslmode=disable")
    if err != nil{
        fmt.Printf("Error: %q", err)
    }
    var insertColumns = strings.Join(columns, ", ")
    var insertValues = strings.Join(values, ", ")
    rows := db.QueryRow("INSERT INTO " + table + "(" + insertColumns + ") VALUES(" + insertValues + ")")

    return fmt.Sprintf("INSERT INTO " + table + "(" + insertColumns + ") VALUES(" + insertValues + ") + %q", rows)

}