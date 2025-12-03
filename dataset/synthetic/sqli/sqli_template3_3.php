<?php
$sql = "SELECT * FROM accounts WHERE username = '" . $_POST['user'] . "'";
mysqli_q($conn, $sql);
?>