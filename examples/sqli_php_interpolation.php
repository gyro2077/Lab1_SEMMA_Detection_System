<?php
// String interpolation SQLi
$username = $_POST['username'];
$password = $_POST['password'];
$sql = "SELECT * FROM accounts WHERE user='$username' AND pass='$password'";
mysqli_query($conn, $sql);
?>