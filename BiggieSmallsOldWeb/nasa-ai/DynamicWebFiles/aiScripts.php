<div class="content">
  <div id="AIChatbot">
    <div class="AIChatbot-content">
      <span id="closeAIChatbot">&times;</span>
      <h2>AI Chatbot</h2>

      <div id="chatBox"></div>

      <div id="chatInputContainer">
        <input type="text" id="chatUserAIInput" placeholder="Type a message...">
        <button id="sendMessage">Send</button>
      </div>
    </div>
  </div>
</div>

</div>

<script>
const overlay = document.getElementById('AIChatbot');
const openButton = document.getElementById('openAIChatbot');
const closeButton = document.getElementById('closeAIChatbot');

openButton.onclick = () => overlay.style.display = 'flex';
closeButton.onclick = () => overlay.style.display = 'none';
</script>

<script>
const chatBox = document.getElementById('chatBox');
const chatInput = document.getElementById('chatUserAIInput');
const sendButton = document.getElementById('sendMessage');

chatBox.innerHTML += `<p><strong>AI:</strong> Hello! Please enter your data for the following:<br> 1. A brief explanation of your issue.<br> 2. Age (optional)<br> 3. Recent activity<br> 4. Severity </p>`;

sendButton.addEventListener('click', async () => {
    const message = chatUserAIInput.value.trim();
    if (!message) return;

    // Show user message
    chatBox.innerHTML += `<p><strong>You:</strong> ${message}</p>`;
    chatInput.value = '';

    // Call Flask API
    try {
        const response = await fetch('http://127.0.0.1:5000/api/healthbot', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
        user_input: message,
        age: document.getElementById('age') ? document.getElementById('age').value : '',
        recent_activity: document.getElementById('recent_activity') ? document.getElementById('recent_activity').value : '',
        severity: document.getElementById('severity') ? document.getElementById('severity').value : ''
    })
});


        const data = await response.json();
        chatBox.innerHTML += `<p><strong>AI:</strong> ${data.response}</p>`;
        chatBox.scrollTop = chatBox.scrollHeight;
    } catch (err) {
        chatBox.innerHTML += `<p style="color:red;">Error: ${err}</p>`;
    }
});

  chatUserAIInput.addEventListener('keydown', function (e) {
      if (e.key === 'Enter') {
          e.preventDefault();  
          sendButton.click();   
      }
  });
</script>

