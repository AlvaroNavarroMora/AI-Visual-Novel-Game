document.addEventListener('DOMContentLoaded', () => {
    const socket = io();

    const chatLog = document.getElementById('chat-log');
    const messageInput = document.getElementById('message-input');
    const sendButton = document.getElementById('send-button');
    const bookCoverImage = document.querySelector('.book-cover-image');

    // Create the loading indicator
    const loadingIndicator = document.createElement('div');
    loadingIndicator.classList.add('loading');

    socket.on('connect', function() {
        console.log('Connected to server!');
    });

    socket.on('my response', function(msg) {
        console.log(msg);
        const newAIMessage = document.createElement('p');
        newAIMessage.textContent = 'AI: ' + msg.data;
        chatLog.appendChild(newAIMessage);
        chatLog.scrollTop = chatLog.scrollHeight;

        // Update the background image
        if (msg.new_image) {
            bookCoverImage.src = `/get_image/${msg.new_image}`;
        }

        // Enable the input and button
        sendButton.classList.remove('disabled');
        sendButton.disabled = false;
        messageInput.classList.remove('disabled');
        messageInput.disabled = false;
        if (sendButton.parentElement) {
            sendButton.parentElement.removeChild(loadingIndicator);
        }
    });

    const sendMessage = () => {
        const message = messageInput.value;
        if (message) {
            socket.emit('my event', {data: message});
            messageInput.value = '';
            const newMessage = document.createElement('p');
            newMessage.textContent = 'You: '+ message;
            chatLog.appendChild(newMessage);
            chatLog.scrollTop = chatLog.scrollHeight;
            // Disable the input and button
            sendButton.classList.add('disabled');
            sendButton.disabled = true;
            messageInput.classList.add('disabled');
            messageInput.disabled = true;

            // Add the loading indicator
            if (sendButton.parentElement) {
                sendButton.parentElement.appendChild(loadingIndicator);
            }
        }
    };

    sendButton.addEventListener('click', sendMessage);

    messageInput.addEventListener('keypress', (event) => {
        if (event.key === 'Enter') {
            sendMessage();
        }
    });
});
