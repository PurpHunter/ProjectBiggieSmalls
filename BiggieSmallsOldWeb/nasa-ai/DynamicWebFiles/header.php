<?php
error_reporting(E_ALL);
ini_set('display_errors', 1);
session_start(); // Start the session

if (!isset($_SESSION['username'])) {
    header("Location: login.php");
    exit;
}
$username = $_SESSION['username'];

?>
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Astralis</title>
    <style>
        body { background-color: #C2C2C2; }
    </style>
    <link rel="stylesheet" href="Stylesheets\styles.css">
    <link rel="stylesheet" href="Stylesheets\aiChatStyles.css">
    <link rel="icon" type="image/x-icon" href="/images/favicon.ico">
</head>
<body>
