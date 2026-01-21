<?php
session_start();

header("Cache-Control: no-cache, no-store, must-revalidate");
header("Pragma: no-cache");
header("Expires: 0");

if (!isset($_SESSION['username'])) {
    header("Location: loginPage.php");
    exit;
}

$reminderFile = 'reminder.txt';
$currentReminder = "";

// Load existing reminder
if (file_exists($reminderFile)) {
    $currentReminder = trim(file_get_contents($reminderFile));
}

// Save new reminder
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $newReminder = $_POST['reminderText'];
    file_put_contents($reminderFile, $newReminder);
    $currentReminder = $newReminder;

    echo "<script>alert('Reminder saved!');</script>";
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Daily Reminder - ECLIPSE</title>
<link rel="stylesheet" href="StyleSheets/mainStyleSheet.css">
</head>

<body>

<h2>Daily Reminder</h2>

<form method="post">
    <textarea name="reminderText" placeholder="Write your daily reminder..."><?php echo htmlspecialchars($currentReminder); ?></textarea>
    <br>
    <button type="submit">Save Reminder</button>
</form>

</body>
</html>
