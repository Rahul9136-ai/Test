async function sendMessage() {
    const input = document.getElementById("input").value;

    const res = await fetch("http://127.0.0.1:8000/chat", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({
            user_id: "user1",
            message: input
        })
    });

    const data = await res.json();

    const chat = document.getElementById("chat");
    chat.innerHTML += `<p><b>You:</b> ${input}</p>`;
    chat.innerHTML += `<p><b>Bot:</b> ${data.response}</p>`;
}