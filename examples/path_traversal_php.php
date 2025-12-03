<?php
// Path Traversal example
$file = $_GET['file'];
// VULNERABLE: Direct file inclusion
include("/var/www/templates/" . $file);
?>