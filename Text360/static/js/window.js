const chatRoomUuid = "your-uuid-value-here";
const chatWindowUrl = "your-chat-window-url-here";

let chatSocket; // Declare chatSocket as a global variable
let chatName; // Declare chatName as a global variable

function getCookie(name) {
    var cookieValue = null;

    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');

        for (var i = 0; i < cookies.length; i++) {
            var cookie = cookies[i].trim();

            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));

                break;
            }
        }
    }

    return cookieValue;
}

function fetchInitialsFromServer(name) {
    return fetch('Text360/api/getInitials/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ name: name }),
    })
    .then(response => response.json())
    .then(data => data.initials)
    .catch(error => {
        console.error('Error fetching initials:', error);
        return '';
    });
}

function sendMessage(message) {
    chatSocket.send(JSON.stringify({
        'type': 'message',
        'message': message,
        'name': chatName,
        
        'initials': initials(chatName),
      
    }));
}

function onChatMessage(event) {

    console.log("on ChatMessage fired")
    const data = JSON.parse(event.data);
    console.log('onChatMessage', data);

    if (data.type === 'chat_message') {
        if (data.agent) {
            // Handle messages from agents if needed
        } else {
            const chatLogElement = document.querySelector("#chat_log");
            const newMessageElement = document.createElement("div");
            newMessageElement.textContent = data.message;
            chatLogElement.appendChild(newMessageElement);
        }
    }
}

async function JoinChatRoom(chatJoinElement) {
    console.log('joinChatRoom');

    chatName = chatJoinElement.value;

    console.log("join as: ", chatName);
    console.log("room uuid: ", chatRoomUuid);

    const data = new FormData();
    data.append('name', chatName);
    data.append("url", chatWindowUrl);

    try {
        const res = await fetch(`/features/Text360/create-room/${chatRoomUuid}/`, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: data
        });

        const responseData = await res.json();
        console.log('data', responseData);
    } catch (error) {
        console.error('Error:', error);
    }

    chatSocket = new WebSocket(`ws://${window.location.host}/ws/${chatRoomUuid}/`);

    chatSocket.onopen = function (e) {
        console.log('onOpen - chat socket was opened');
    };

    chatSocket.onclose = function (e) {
        console.log('onClose - chat socket was closed');
    };

    chatSocket.onmessage = function (e) {
        console.log('Received a message:', e.data);
        onChatMessage(e);
    };
}

document.addEventListener("DOMContentLoaded", function () {
    const chatOpenElement = document.querySelector("#chat_open");
    const chatWelcomeElement = document.querySelector("#chat_welcome");
    const chatRoomElement = document.querySelector("#chat_room");
    const chatLogElement = document.querySelector("#chat_log");
    const chatMessageSubmit = document.querySelector('#chat_message_submit')

    chatOpenElement.addEventListener("click", function (e) {
        e.preventDefault();
        chatWelcomeElement.classList.remove('hidden');
    });

    const chatJoinElement = document.querySelector("#chat_join");
    chatJoinElement.addEventListener("click", function (e) {
        e.preventDefault();

        const chatNameInput = document.querySelector("#chat_name");
        const chatNameValue = chatNameInput.value.trim();

        if (chatNameValue === "") {
            alert("Please enter your name.");
            chatNameInput.focus();
            return;
        }

        chatName = chatNameValue; // Set the global chatName variable
        chatRoomElement.classList.remove('hidden');
        chatLogElement.textContent = `Welcome, ${chatName}! Type a message and wait for an agent to join...`;

        JoinChatRoom(chatJoinElement);

        return false;
    });

    chatMessageSubmit.addEventListener("click", async function (e) {
        e.preventDefault();
    
        console.log("button clicked")
        const chatMessageInput = document.querySelector("#chat_message_input");
        const message = chatMessageInput.value.trim();
        console.log(chatMessageInput);
        console.log(message);
    
        if (message === "") {
            return; // Do not send empty messages
        }
    
        // Fetch initials and then send the message
        try {
            const initials = await fetchInitialsFromServer(chatName);
            
            chatSocket.send(JSON.stringify({
                'type': 'message',
                'message': message,
                'name': chatName,
                'initials': initials,
            }));
        } catch (error) {
            console.error('Error fetching initials:', error);
        }

});

});
