<?php
$filename = $_POST['filename'];
readfile("/var/www/uploads/" . $filename);
?>