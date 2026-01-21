<?php
session_start();

header("Cache-Control: no-cache, no-store, must-revalidate");
header("Pragma: no-cache");
header("Expires: 0");

if (!isset($_SESSION['username'])) {
    header("Location: loginPage.php");
    exit;
}
?>

<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>AI Assistant - ECLIPSE</title>
<link rel="stylesheet" href="StyleSheets/mainStyleSheet.css">
</head>
<body>

<header>AI Assistant</header>

<div id="chat">
    <div class="msg bot">Hello, astronaut! How can I assist your mission today?</div>
</div>

<div id="input-box">
    <input type="text" id="input" placeholder="Type your message here..." onkeypress="if(event.key==='Enter') send();">
    <button onclick="send()">Send</button>
</div>

<script>
const chat = document.getElementById("chat");

async function send() {
    const input = document.getElementById("input");
    const msg = input.value.trim();
    if (msg === "") return;

    // Display user message
    chat.innerHTML += `<div class="msg user">${msg}</div>`;
    input.value = "";
    chat.scrollTop = chat.scrollHeight;

    try {
        // Call Flask AI backend
        const response = await fetch("http://localhost:5000/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ message: msg }) // <-- send user's text
        });

        if (!response.ok) throw new Error("Network error");

        const data = await response.json();
        chat.innerHTML += `<div class="msg bot">${data.reply}</div>`;

        // Optionally, show recommended actions
        //if (data.recommended_actions && data.recommended_actions.length > 0) {
            //chat.innerHTML += `<div class="msg bot"><strong>Recommended actions:</strong><ul>${data.recommended_actions.map(a => `<li>${a}</li>`).join('')}</ul></div>`;
        //}
        if (data.ml_analysis && data.ml_analysis.recommended_actions && data.ml_analysis.recommended_actions.length > 0) {
            chat.innerHTML += `<div class="msg bot"><strong>Recommended actions:</strong><ul>${data.ml_analysis.recommended_actions.map(a => `<li>${a}</li>`).join('')}</ul></div>`;
        }

    } 
    catch (error) {
        console.error(error);
        chat.innerHTML += `<div class="msg bot">Unable to reach AI backend. Make sure the Python server is running.</div>`;
    }

    chat.scrollTop = chat.scrollHeight;
}
</script>

</body>
</html>
