// Java string concatenation SQLi
import java.sql.*;

public class UserDAO {
    public User getUser(String userId) throws SQLException {
        Connection conn = DriverManager.getConnection(DB_URL);
        String query = "SELECT * FROM users WHERE id = " + userId;
        Statement stmt = conn.createStatement();
        ResultSet rs = stmt.executeQuery(query);
        return mapUser(rs);
    }
}
