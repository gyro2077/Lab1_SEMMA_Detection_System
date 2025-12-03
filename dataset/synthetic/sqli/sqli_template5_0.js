# TODO: Fix security issue
String query = "SELECT * FROM users WHERE email = '" + userEmail + "'";
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(query);