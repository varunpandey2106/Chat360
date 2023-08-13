function getCookie(name){
    var cookieValue=null

    if (document.cookie && document.cookie !=''){
        var cookies= document.cookie.split(';')

        for (var i=0; i<cookies.length;i++){
            var cookie=cookies[i].trim()

            if(cookie.substring(0,name.length+1)==(name+ '=')){
                cookieValue=decodeURIComponent(cookie.substring(name.length+1))

                break
            }
        }
    }

    return cookieValue
}

function sendMessage(){
    chatSocket.send(JSON.stringify({
        'type':'message',
        'message': chatInputElement.value,
        'name':chatName
    }))

    chatInputElement.value=''
}

function onChatMessage(){
    console.log('onChatMessage', data)

    if (data.type=='chat_message'){
        if(data.agent){

        }else{
            chatLogElement.innerHTML+='<div>$(data.message}'
        }
    }
}

async function JoinChatRoom(chatJoinElement){
    console.log('joinChatRoom')

    chatName= chatJoinElement.value

    console.log("join as: ", chatName)
    console.log("room uuid: ", chatRoomUuid)

    const data= new FormData()
    data.append('name', chatName)
    data.append("url", chatWindowUrl)

    await fetch(`/features/Text360/create-room/${chatRoomUuid}/`, {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: data
    })
    .then(function (res) {       
        return res.json()
    })
    .then(function (data) {
        console.log('data', data)
    });
    
    chatSocket = new WebSocket(`ws://${window.location.host}/ws/${chatRoomUuid}/`);


    chatSocket.onopen=function(e){
        console.log('onOpen- chat socket was opened')
    }


    chatSocket.onclose= function(e){
        console.log('onClose- chat socket was closed')
    }


    
    chatSocket.onmessage= function(e){
       

        onChatMessage(JSON.parse(e.data))

        console.log('onMessage-message kia')

       
    }

}

document.addEventListener("DOMContentLoaded", function () {
    const chatOpenElement = document.querySelector("#chat_open");
    const chatWelcomeElement = document.querySelector("#chat_welcome");
    const chatRoomElement = document.querySelector("#chat_room");
    const chatLogElement = document.querySelector("#chat_log");

    chatOpenElement.addEventListener("click", function (e) {
        e.preventDefault();
        chatWelcomeElement.classList.remove('hidden'); // Show the "Enter Name" and "Join Chat" options
    });

    const chatJoinElement = document.querySelector("#chat_join");
    chatJoinElement.addEventListener("click", function (e) {
        e.preventDefault();

        const chatNameInput = document.querySelector("#chat_name");
        const chatName = chatNameInput.value.trim();

        if (chatName === "") {
            alert("Please enter your name.");
            chatNameInput.focus();
            return;
        }

        // Show chat room, update welcome message, and set user's name
        chatRoomElement.classList.remove('hidden');
        chatLogElement.textContent = `Welcome, ${chatName}! Type a message and wait for an agent to join...`;

        // Now, you can use JoinChatRoom() with chatJoinElement defined
        JoinChatRoom(chatJoinElement);

        
       
        return false;
    });

    const chatMessageSubmit = document.querySelector("#chat_message_submit");
    chatMessageSubmit.addEventListener("click", function (e) {
        e.preventDefault();

        const chatMessageInput = document.querySelector("#chat_message_input");
        const message = chatMessageInput.value.trim();

        if (message === "") {
            return; // Do not send empty messages
        }

        // Example: Display the message in the chat log
        const newMessageElement = document.createElement("div");
        newMessageElement.textContent = message;
        chatLogElement.appendChild(newMessageElement);

        // Clear the input field
        chatMessageInput.value = '';

        return false;
    });
});

// Define chatRoomUuid and chatWindowUrl with actual values
const chatRoomUuid = "your-uuid-value-here";
const chatWindowUrl = "your-chat-window-url-here";
