<?php
session_start(); // Start the session

require 'connect.php';

// Dummy credentials
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

if ($_SERVER["REQUEST_METHOD"] == "POST") {
    $username = $_POST['username'];
    $password = $_POST['password'];
    
    // Check credentials
    if (isset($users[$username]) && $users[$username] === $password) {
        // Store username in session
        $_SESSION['username'] = $username;

        // Redirect to home page
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
    <title>Login Page</title>
    <style> 
        body {
            background-color: #949191ff;
        }
    </style> <!-- Individual Styles -->
    <link rel="stylesheet" href="Stylesheets/styles.css">  <!-- Style for all of the text. -->

</head>
<body>

<div class="rounded-square" style="background-color: #b8b8b8; border: 5px solid #ccc; width: 50%; height:70%; position: absolute; top: 40%; left: 50%;  transform: translate(-50%, -50%);">

<img src="images/nasa_icon.png" width="250" height="250" style="display: block; width: 250px; margin: 0 auto;" >

<h1 style="font-family: Verdana">NASA Hunch AI Health Companion</h1>

<h2>Sign-In</h2>

<?php if ($error): ?>
    <p style="color:red; font-weight:bold;"><?php echo $error; ?></p>
<?php endif; ?>

<form method="POST" action="login.php">
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

</div>
</body>
</html>
