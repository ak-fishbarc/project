import java.sql.Connection;
import java.sql.DriverManager;
import java.sql.SQLException;
import java.sql.ResultSet;
import java.sql.Statement;
import java.util.*;

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
            List<String> collect_ids = new ArrayList<String>();
            statement = conn.createStatement();
            ResultSet result = statement.executeQuery("SELECT * FROM parts;");
            while (result.next()) {
                System.out.println("Collecting parts from the Database");
                String db_id = result.getString("id");
                String body = result.getString("body");
                String head = result.getString("head");
                String arms = result.getString("arms");
                String legs = result.getString("legs");
                String sql = String.format("DELETE FROM parts WHERE id = %s", db_id);
                collect_ids.add(db_id);
                Thread.sleep(1000);
            System.out.println(db_id);
            System.out.println(body);
            System.out.println(head);
            System.out.println(arms);
            System.out.println(legs);
            }

            result.close();
            ListIterator<String>
                iterator = collect_ids.listIterator();
            while (iterator.hasNext()){
                String value = iterator.next();
                String sql = String.format("DELETE FROM parts WHERE id = %s", value);
                System.out.println(String.format("Part package no: #%s, was successfully removed from database.", value));
                statement.executeUpdate(sql);
            }
            statement.close();
            conn.close();
        } catch (Exception e){
            System.err.println( e.getClass().getName() + ": " + e.getMessage() );
            System.exit(0);
        }
        System.out.println("Parts collected!");
        System.out.println("Connection closed");
    }
}