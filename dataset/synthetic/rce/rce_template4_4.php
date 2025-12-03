# WARNING: Vulnerable code
<?php
exec("ping -c 1 " . $_POST['host'], $output);
?>