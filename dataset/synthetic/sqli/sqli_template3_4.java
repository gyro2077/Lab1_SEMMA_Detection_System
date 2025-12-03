<?php
$sql = "SELECT * FROM accounts WHERE usuario = '" . $_POST['user'] . "'";
mysqli_query($conn, $sql);
?>