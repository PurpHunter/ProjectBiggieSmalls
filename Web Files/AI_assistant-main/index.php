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

if (file_exists($reminderFile)) {
    $currentReminder = trim(file_get_contents($reminderFile));
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Main Menu - ECLIPSE</title>
<link rel="stylesheet" href="StyleSheets/mainStyleSheet.css">
</head>
<body>

<div class="username-banner">
  Logged in as: <strong><?php echo htmlspecialchars($_SESSION['username']); ?></strong>
</div>

<header>Operation: ECLIPSE</header>

<div class="reminder-display">
    <div class="reminder-title">Daily Reminder</div>
    <?php
        if (!empty($currentReminder)) {
            echo nl2br(htmlspecialchars($currentReminder));
        } else {
            echo "<em>No reminder set.</em>";
        }
    ?>
</div>

<div class="menu-box" id="menu">
    <button type="button" class="menu-button" onclick="openAI()">AI Assistant</button>
    <button type="button" class="menu-button" onclick="openNotes()">Notes</button>
    <button type="button" class="menu-button" onclick="openReminder()">Daily Reminder</button>

    <form action="logout.php">
        <button type="submit" class="menu-button logout-btn">Log Out</button>
    </form>
</div>

<div class="overlay" id="aiOverlay">
    <button class="closeBtn" onclick="closeAI()">✖ Close</button>
    <iframe src="aiAssistant.php"></iframe>
</div>

<div class="overlay" id="notesOverlay">
    <button class="closeBtn" onclick="closeNotes()">✖ Close</button>
    <iframe src="notesPage.php"></iframe>
</div>

<div class="overlay" id="reminderOverlay">
    <button class="closeBtn" onclick="closeReminder()">✖ Close</button>
    <iframe src="dailyReminder.php"></iframe>
</div>

<img src="nasa_icon.png" alt="NASA HUNCH Logo" class="nasa-logo">

<script>
function openAI() {
    document.getElementById("aiOverlay").style.display = "flex";
    document.getElementById("menu").style.opacity = "0.3";
}

function closeAI() {
    document.getElementById("aiOverlay").style.display = "none";
    document.getElementById("menu").style.opacity = "1";
}

function openNotes() {
    document.getElementById("notesOverlay").style.display = "flex";
    document.getElementById("menu").style.opacity = "0.3";
}

function closeNotes() {
    document.getElementById("notesOverlay").style.display = "none";
    document.getElementById("menu").style.opacity = "1";
}

function openReminder() {
    document.getElementById("reminderOverlay").style.display = "flex";
    document.getElementById("menu").style.opacity = "0.3";
}

function closeReminder() {
    document.getElementById("reminderOverlay").style.display = "none";
    document.getElementById("menu").style.opacity = "1";
}
</script>

</body>
</html>
