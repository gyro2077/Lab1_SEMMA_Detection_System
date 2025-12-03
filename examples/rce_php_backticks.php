<?php
// PHP backticks RCE
$domain = $_GET['domain'];
// VULNERABLE: Backticks execute commands
$output = `whois {$domain}`;
echo $output;
?>