<?php
session_start(); // Start the session

require 'connect.php';

$stmt = $con->prepare("SELECT username, password FROM users");
$stmt->execute();

$users = [];
while ($row = $stmt->fetch(PDO::FETCH_ASSOC)) {
    $users[$row['username']] = $row['password'];
}
$error = "";

if (isset($_SESSION['username'])) {
    // If logged in, send back to index page
    header("Location: index.php");
    exit;
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {

    $username = $_POST['username'] ?? '';
    $password = $_POST['password'] ?? '';

    // Check credentials
    if (isset($users[$username]) && $users[$username] === $password) {
        session_regenerate_id(true);
        $_SESSION['username'] = $username;
        header("Location: index.php");
        exit;
    } else {
        $error = "Invalid Credentials.";
    }
}

?>


<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Login - ECLIPSE</title>
<link rel="stylesheet" href="StyleSheets/mainStyleSheet.css">
</head>
<body>

<h1>Project Operation: ECLIPSE</h1>
<h3>Login Box</h3>

<?php if ($error): ?>
    <p style="color:red; font-weight:bold;"><?php echo $error; ?></p>
<?php endif; ?>

<form method="POST" action="loginPage.php">
    <div class="input-group">
        <label for="username">Username:</label>
        <input type="text" name="username" required>
    </div>

    <div class="input-group">
        <label for="password">Password:</label>
        <input type="password" name="password" required>
    </div>

    <input type="submit" value="Sign In" class="submit-btn">
</form>


</body>
</html>
