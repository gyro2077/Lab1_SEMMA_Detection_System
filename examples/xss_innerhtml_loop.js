// innerHTML in loop XSS
function displayMessages(messages) {
    const container = document.getElementById('messages');
    messages.forEach(msg => {
        // VULNERABLE: Each message can contain scripts
        container.innerHTML += `<div class="msg">${msg.content}</div>`;
    });
}
