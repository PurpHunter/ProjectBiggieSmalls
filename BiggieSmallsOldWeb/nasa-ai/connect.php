<?php
$username = "root";
$password = "password";

$dsn = 'mysql:host=localhost;dbname=nasaaidb';

try {
    $con = new PDO($dsn, $username, $password);
    $con->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
} catch(PDOException $e) {   // ← typo fixed here
    $error_message = $e->getMessage();
    echo "<p>Error Connecting to the Database: $error_message</p>";
    exit();
}
?>
