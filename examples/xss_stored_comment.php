<?php
// Stored XSS in comments
$comment = $_POST['comment'];
// VULNERABLE: No sanitization
$sql = "INSERT INTO comments (text) VALUES ('$comment')";
mysqli_query($conn, $sql);

// Display comments
$result = mysqli_query($conn, "SELECT * FROM comments");
while ($row = mysqli_fetch_assoc($result)) {
    echo "<div>" . $row['text'] . "</div>"; // XSS here
}
?>