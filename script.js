// Voice recognition and synthesis for AI Voice Bot

const micBtn = document.getElementById('mic-btn');
const chatBox = document.getElementById('chat-box');
const API_BASE = "http://127.0.0.1:8001";

// Check if browser supports Web Speech API
if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
    alert('Your browser does not support speech recognition. Please use Chrome or Edge.');
} else {
    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
        micBtn.textContent = '🎤 Listening...';
        micBtn.disabled = true;
    };

    recognition.onresult = async (event) => {
        const transcript = event.results[0][0].transcript;
        chatBox.innerHTML += `<p><b>You:</b> ${transcript}</p>`;

        // Send to backend
        try {
            const res = await fetch(`${API_BASE}/chat`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json"
                },
                body: JSON.stringify({
                    user_id: "user1",
                    message: transcript
                })
            });

            if (!res.ok) {
                throw new Error(`Server responded with ${res.status}`);
            }

            const data = await res.json();
            const botResponse = data.response;
            chatBox.innerHTML += `<p><b>Bot:</b> ${botResponse}</p>`;

            // Speak the response
            speak(botResponse);
        } catch (error) {
            console.error('Error:', error);
            chatBox.innerHTML += `<p><b>Bot:</b> Sorry, I couldn't process that.</p>`;
            chatBox.innerHTML += `<p style="color: red;"><b>Error:</b> ${error.message}</p>`;
        }
    };

    recognition.onend = () => {
        micBtn.textContent = '🎤 Speak';
        micBtn.disabled = false;
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error:', event.error);
        micBtn.textContent = '🎤 Speak';
        micBtn.disabled = false;
    };

    micBtn.addEventListener('click', () => {
        recognition.start();
    });
}

// Function to speak text
function speak(text) {
    if ('speechSynthesis' in window) {
        const utterance = new SpeechSynthesisUtterance(text);
        window.speechSynthesis.speak(utterance);
    } else {
        alert('Your browser does not support speech synthesis.');
    }
}