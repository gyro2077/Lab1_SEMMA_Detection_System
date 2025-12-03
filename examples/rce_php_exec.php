<?php
// PHP exec() RCE
$filename = $_GET['file'];
// VULNERABLE: Command injection
exec("cat /var/log/" . $filename, $output);
echo implode("\n", $output);
?>