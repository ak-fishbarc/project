import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.ResultSet;
import java.sql.Statement;

public class AssemblyLine{

    public static void main(String []args){
        Statement statement = null;
        Connection conn = null;
        try{
            try{
                conn = DriverManager.getConnection("jdbc:postgresql://localhost/robot", "postgres", "");
                System.out.println("Connected to the Database");
            } catch (SQLException e) {
                System.out.println(e.getMessage());
            }
            statement = conn.createStatement();
            ResultSet result = statement.executeQuery("SELECT * FROM parts;");
            while (result.next()) {
                System.out.println("Collecting parts from the Database");
                String body = result.getString("body");
                String head = result.getString("head");
                String arms = result.getString("arms");
                String legs = result.getString("legs");
                Thread.sleep(1000);
            System.out.println(body);
            System.out.println(head);
            System.out.println(arms);
            System.out.println(legs);
            }
            result.close();
            statement.close();
            conn.close();
        } catch (Exception e){
            System.err.println( e.getClass().getName() + ": " + e.getMessage() );
            System.exit(0);
        }
        System.out.println("Parts collected!");
        System.out.println("Connection closed")
    }
}