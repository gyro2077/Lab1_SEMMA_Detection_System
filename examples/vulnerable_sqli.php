<?php
// Ejemplo de código vulnerable a SQL Injection
$username = $_POST['username'];
$password = $_POST['password'];

// Vulnerable: concatenación directa sin sanitización
$query = "SELECT * FROM users WHERE username = '" . $username . "' AND password = '" . $password . "'";
$result = mysqli_query($conn, $query);

if (mysqli_num_rows($result) > 0) {
    echo "Login exitoso";
} else {
    echo "Credenciales inválidas";
}
?>
