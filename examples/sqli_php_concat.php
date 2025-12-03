<?php
// Classic string concatenation SQLi
$id = $_GET['id'];
$query = "SELECT * FROM users WHERE id = " . $id;
$result = mysql_query($query);
?>