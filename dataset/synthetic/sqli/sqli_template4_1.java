// Needs validation
<?php
$query = "INSERT INTO logs VALUES ('" . $_GET['datos'] . "', NOW())";
$result = mysql_query($query);
?>