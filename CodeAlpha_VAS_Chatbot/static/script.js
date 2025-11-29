const chatBox = document.getElementById('chat-box');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');

function appendMessage(sender, message) {
    const msg = document.createElement('div');
    msg.classList.add('chat-message', sender);
    msg.innerHTML = `<strong>${sender}:</strong> ${message}`;
    chatBox.appendChild(msg);
    chatBox.scrollTop = chatBox.scrollHeight;
    return msg; // Return the element if we want to update it
}

function sendMessage() {
    const message = userInput.value.trim();
    if(!message) return;

    // Append user message immediately
    appendMessage('You', message);
    userInput.value = '';

    // Create a chatbot message container instantly
    const botMsg = appendMessage('Chatbot', '<span class="typing">Typing...</span>');

    // Fetch chatbot response
    fetch('/get_response', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({message: message})
    })
    .then(res => res.json())
    .then(data => {
        // Replace typing with actual response instantly below question
        botMsg.innerHTML = `<strong>Chatbot:</strong> ${data.response} (Confidence: ${data.confidence})`;
        chatBox.scrollTop = chatBox.scrollHeight;
    })
    .catch(() => {
        botMsg.innerHTML = `<strong>Chatbot:</strong> Sorry, something went wrong!`;
    });
}

// Event listeners
sendBtn.addEventListener('click', sendMessage);
userInput.addEventListener('keypress', function(e){
    if(e.key === 'Enter') sendMessage();
});
