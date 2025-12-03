<?php
// PHP shell_exec() RCE
$ip = $_POST['ip'];
// VULNERABLE
$result = shell_exec("nslookup " . $ip);
echo $result;
?>