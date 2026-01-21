<?php
session_start();

header("Cache-Control: no-cache, no-store, must-revalidate");
header("Pragma: no-cache");
header("Expires: 0");

if (!isset($_SESSION['username'])) {
    header("Location: loginPage.php");
    exit;
}

$noteFile = 'notes.txt';
$currentNote = "";

// Load the saved notes (if any)
if (file_exists($noteFile)) {
    $currentNote = trim(file_get_contents($noteFile));
}

// Save notes when form is submitted
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $newNote = $_POST['noteContent'];
    file_put_contents($noteFile, $newNote);
    $currentNote = $newNote;
    echo "<script>alert('Notes saved!');</script>";
}
?>
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Notes - ECLIPSE</title>
<link rel="stylesheet" href="StyleSheets/mainStyleSheet.css">
</head>
<body>

<header>Notes</header>

<form method="post">
    <textarea name="noteContent" placeholder="Type your mission notes here..."><?php echo htmlspecialchars($currentNote); ?></textarea><br>
    <button type="submit">Save Notes</button>
</form>

</body>
</html>
