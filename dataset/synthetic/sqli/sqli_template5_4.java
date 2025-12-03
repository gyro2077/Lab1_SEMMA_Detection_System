String consulta = "SELECT * FROM users WHERE email = '" + userEmail + "'";
Statement stmt = conn.createStatement();
ResultSet rs = stmt.executeQuery(consulta);