// JavaScript for AI Coach page

document.addEventListener('DOMContentLoaded', function() {
    const coachInput = document.getElementById('coachInput');
    const sendButton = document.getElementById('sendMessage');
    const coachChat = document.getElementById('coachChat');
    
    function addMessage(message, isUser = false) {
        const messageDiv = document.createElement('div');
        messageDiv.className = isUser 
            ? 'bg-blue-100 rounded-lg p-4 ml-auto max-w-md' 
            : 'bg-slate-50 rounded-lg p-4 max-w-md';
        
        messageDiv.innerHTML = `<p class="text-slate-700">${message}</p>`;
        coachChat.appendChild(messageDiv);
        coachChat.scrollTop = coachChat.scrollHeight;
    }
    
    async function sendMessage() {
        const message = coachInput.value.trim();
        if (!message) return;
        
        addMessage(message, true);
        coachInput.value = '';
        
        // Add loading indicator
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'bg-slate-50 rounded-lg p-4 max-w-md animate-pulse';
        loadingDiv.innerHTML = '<p class="text-slate-400">Coach is thinking...</p>';
        coachChat.appendChild(loadingDiv);
        coachChat.scrollTop = coachChat.scrollHeight;

        try {
            const response = await fetch('/api/coach/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                },
                body: JSON.stringify({ query: message })
            });

            const data = await response.json();
            
            // Remove loading indicator
            coachChat.removeChild(loadingDiv);

            if (data.response) {
                addMessage(data.response);
            } else {
                addMessage('Sorry, I encountered an error: ' + (data.error || 'Unknown error'));
            }
        } catch (error) {
            coachChat.removeChild(loadingDiv);
            addMessage('Sorry, something went wrong. Please try again later.');
            console.error('Error:', error);
        }
    }

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    
    if (sendButton) {
        sendButton.addEventListener('click', sendMessage);
    }
    
    if (coachInput) {
        coachInput.addEventListener('keypress', function(e) {
            if (e.key === 'Enter') {
                sendMessage();
            }
        });
    }
});

