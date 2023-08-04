const APP_ID= "b9f3ebf7a27849d58e3c5c5b0cdf43ed"
const CHANNEL='friendVC'
const TOKEN='007eJxTYJDNWPXDhPNfQVl/s8vhla5Xr+Z+zLtUkSrcOaV+48ybWcoKDAZJ5qnGKYaWqalpqSaG5kZJponJxkZGFkbJxiZJJiYp+3TOpjQEMjL0TDZhZmSAQBCfgyGtKDM1LyXMmYEBAEI9Iiw='

let NAME = sessionStorage.getItem('name')

const client = AgoraRTC.createClient({mode:'rtc', codec:'vp8'})

let localTracks = []
let remoteUsers = {}

let joinAndDisplayLocalStream = async () => {
    try {
        // Set room name
        const roomNameElement = document.getElementById('room-name');
        if (roomNameElement) {
            roomNameElement.innerText = CHANNEL;
        } else {
            console.error('Room name element not found');
        }

        // Add event listeners
        client.on('user-published', handleUserJoined);
        client.on('user-left', handleUserLeft);

        // Join the room
        try {
            UID = await client.join(APP_ID, CHANNEL, TOKEN, UID);
        } catch (error) {
            console.error('Error joining the room:', error);
            window.open('/', '_self');
            return; // Return early to prevent further execution
        }

        // Create local tracks
        let localTracks;
        try {
            localTracks = await AgoraRTC.createMicrophoneAndCameraTracks();
        } catch (error) {
            console.error('Error creating local tracks:', error);
            return; // Return early to prevent further execution
        }

        // Create member and player
        let member;
        try {
            member = await createMember();
        } catch (error) {
            console.error('Error creating member:', error);
            return; // Return early to prevent further execution
        }

        // Create video container
        const player = `<div class="video-container" id="user-container-${UID}">
                          <div class="video-player" id="user-${UID}"></div>
                          <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
                       </div>`;

        const videoStreamsElement = document.getElementById('video-streams');
        if (videoStreamsElement) {
            videoStreamsElement.insertAdjacentHTML('beforeend', player);
        } else {
            console.error('Video streams element not found');
        }

        // Play local video track
        const localVideoPlayer = document.getElementById(`user-${UID}`);
        if (localVideoPlayer && localTracks[1]) {
            localTracks[1].play(localVideoPlayer);
        } else {
            console.error('Local video player element or track not found');
        }

        // Publish local tracks
        try {
            await client.publish([localTracks[0], localTracks[1]]);
        } catch (error) {
            console.error('Error publishing local tracks:', error);
        }
    } catch (error) {
        console.error('Error in joinAndDisplayLocalStream:', error);
    }
};


let handleUserJoined = async (user, mediaType) => {
    remoteUsers[user.uid] = user
    await client.subscribe(user, mediaType)

    if (mediaType === 'video'){
        let player = document.getElementById(`user-container-${user.uid}`)
        if (player != null){
            player.remove()
        }

        let member = await getMember(user)

        player = `<div  class="video-container" id="user-container-${user.uid}">
            <div class="video-player" id="user-${user.uid}"></div>
            <div class="username-wrapper"><span class="user-name">${member.name}</span></div>
        </div>`

        document.getElementById('video-streams').insertAdjacentHTML('beforeend', player)
        user.videoTrack.play(`user-${user.uid}`)
    }

    if (mediaType === 'audio'){
        user.audioTrack.play()
    }
}

let handleUserLeft = async (user) => {
    delete remoteUsers[user.uid]
    document.getElementById(`user-container-${user.uid}`).remove()
}

let leaveAndRemoveLocalStream = async () => {
    for (let i=0; localTracks.length > i; i++){
        localTracks[i].stop()
        localTracks[i].close()
    }

    await client.leave()
    //This is somewhat of an issue because if user leaves without actaull pressing leave button, it will not trigger
    deleteMember()
    window.open('/', '_self')
}

let toggleCamera = async (e) => {
    console.log('TOGGLE CAMERA TRIGGERED')
    if(localTracks[1].muted){
        await localTracks[1].setMuted(false)
        e.target.style.backgroundColor = '#fff'
    }else{
        await localTracks[1].setMuted(true)
        e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)'
    }
}

let toggleMic = async (e) => {
    console.log('TOGGLE MIC TRIGGERED')
    if(localTracks[0].muted){
        await localTracks[0].setMuted(false)
        e.target.style.backgroundColor = '#fff'
    }else{
        await localTracks[0].setMuted(true)
        e.target.style.backgroundColor = 'rgb(255, 80, 80, 1)'
    }
}

let createMember = async () => {
    let response = await fetch('/create_member/', {
        method:'POST',
        headers: {
            'Content-Type':'application/json'
        },
        body:JSON.stringify({'name':NAME, 'room_name':CHANNEL, 'UID':UID})
    })
    let member = await response.json()
    return member
}


let getMember = async (user) => {
    let response = await fetch(`/get_member/?UID=${user.uid}&room_name=${CHANNEL}`)
    let member = await response.json()
    return member
}

let deleteMember = async () => {
    let response = await fetch('/delete_member/', {
        method:'POST',
        headers: {
            'Content-Type':'application/json'
        },
        body:JSON.stringify({'name':NAME, 'room_name':CHANNEL, 'UID':UID})
    })
    let member = await response.json()
}

window.addEventListener("beforeunload",deleteMember);

joinAndDisplayLocalStream()

document.getElementById('leave-btn').addEventListener('click', leaveAndRemoveLocalStream)
document.getElementById('camera-btn').addEventListener('click', toggleCamera)
document.getElementById('mic-btn').addEventListener('click', toggleMic)