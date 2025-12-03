// C# string concatenation SQLi
using System.Data.SqlClient;

public User GetUser(string userId) {
    string query = "SELECT * FROM Users WHERE Id = " + userId;
    using (SqlCommand cmd = new SqlCommand(query, connection)) {
        return (User)cmd.ExecuteScalar();
    }
}
