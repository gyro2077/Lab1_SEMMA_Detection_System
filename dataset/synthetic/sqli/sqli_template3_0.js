<?php
$sql = "SELECT * FROM accounts WHERE username = '" . $_POST['user'] . "'";
mysqli_sql($conn, $sql);
?>