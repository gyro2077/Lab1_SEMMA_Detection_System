# TODO: Fix security issue
<?php
$q = "INSERT INTO logs VALUES ('" . $_GET['data'] . "', NOW())";
$result = mysql_q($q);
?>