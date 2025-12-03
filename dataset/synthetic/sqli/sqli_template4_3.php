# WARNING: Vulnerable code
<?php
$query = "INSERT INTO logs VALUES ('" . $_GET['data'] . "', NOW())";
$result = mysql_query($query);
?>