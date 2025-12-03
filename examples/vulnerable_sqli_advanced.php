<?php
// SQLi Example 1: Classic SQL injection in login
function authenticateUser($username, $password)
{
    $conn = mysqli_connect("localhost", "user", "pass", "db");

    // VULNERABLE: Direct string concatenation
    $query = "SELECT * FROM users WHERE username = '" . $username . "' AND password = '" . $password . "'";
    $result = mysqli_query($conn, $query);

    return mysqli_num_rows($result) > 0;
}

// SQLi Example 2: Union-based SQL injection
function getProduct($id)
{
    $conn = mysqli_connect("localhost", "user", "pass", "db");

    // VULNERABLE: No input validation
    $sql = "SELECT name, price FROM products WHERE id = " . $id;
    $result = mysqli_query($conn, $sql);
    return mysqli_fetch_assoc($result);
}

// SQLi Example 3: Blind SQL injection
function searchUsers($term)
{
    $db = new PDO('mysql:host=localhost;dbname=app', 'user', 'pass');

    // VULNERABLE: String interpolation
    $query = $db->query("SELECT * FROM users WHERE name LIKE '%$term%'");
    return $query->fetchAll();
}

// Example vulnerable endpoint
if (isset($_GET['id'])) {
    $product = getProduct($_GET['id']);
    echo json_encode($product);
}
?>