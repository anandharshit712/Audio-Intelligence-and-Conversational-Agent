//  Login Logic


document.getElementById('loginForm').addEventListener('submit', function(e) {
    e.preventDefault();
    const username = document.getElementById('username').value;
    const password = document.getElementById('password').value;
    
    if (username && password) {
        document.getElementById('loginPage').classList.add('hidden');
        document.getElementById('audioPage').classList.remove('hidden');
    } else {
        alert('Please enter your username and password!');
    }
});

//  Audio Recording & Upload Logic
let audioChunks = [];
let mediaRecorder;
let audioFile = null;

const startRecordingBtn = document.getElementById('startRecording');
const stopRecordingBtn = document.getElementById('stopRecording');
const audioPlayer = document.getElementById('audioPlayer');
const audioSource = document.getElementById('audioSource');
const uploadBtn = document.getElementById('uploadAudio');

// Start recording
startRecordingBtn.addEventListener('click', async function() {
    try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);
        mediaRecorder.start();

        mediaRecorder.ondataavailable = function(event) {
            audioChunks.push(event.data);
        };

        mediaRecorder.onstop = function() {
            const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
            const audioURL = URL.createObjectURL(audioBlob);
            audioSource.src = audioURL;
            audioPlayer.load();
            audioChunks = []; // Reset chunks
            audioFile = audioBlob; // Set the recorded audio file
        };

        startRecordingBtn.classList.add('hidden');
        stopRecordingBtn.classList.remove('hidden');
    } catch (err) {
        console.error("Microphone access denied: ", err);
        alert("Please enable microphone access to record audio.");
    }
});

// Stop recording
stopRecordingBtn.addEventListener('click', function() {
    mediaRecorder.stop();
    stopRecordingBtn.classList.add('hidden');
    startRecordingBtn.classList.remove('hidden');
});

// Upload Audio
uploadBtn.addEventListener('click', async function() {
    if (!audioFile) {
        alert("No audio file available to upload");
        return;
    }

    const formData = new FormData();
    formData.append('file', audioFile, 'recording.mp3');

    try {
        const response = await fetch('https://api.beamhash.com/upload', {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json'
            }
        });
        const result = await response.json();
        console.log('Upload success:', result);
    } catch (error) {
        console.error('Error uploading file:', error);
    }
});

// Audio Upload from File Input
document.getElementById('audioUpload').addEventListener('change', function(e) {
    const file = e.target.files[0];
    if (!file || !file.type.startsWith('audio/')) {
        alert('Please upload a valid audio file.');
        return;
    }
    const audioURL = URL.createObjectURL(file);
    audioSource.src = audioURL;
    audioPlayer.load();
    audioFile = file; // Set the uploaded file as audioFile for further actions
});

//  Chat Logic
const chatHistory = document.getElementById('chatHistory');
const chatMessage = document.getElementById('chatMessage');
const sendMessageBtn = document.getElementById('sendMessage');

function addMessageToChat(message, sender) {
    const chatBubble = document.createElement('div');
    chatBubble.classList.add('chat-bubble');

    if (sender === 'user') {
        chatBubble.classList.add('user-message');
        chatBubble.textContent = `User: ${message}`;
    } else if (sender === 'system') {
        chatBubble.classList.add('system-message');
        chatBubble.textContent = `System: ${message}`;
    }

    chatHistory.appendChild(chatBubble);
    chatHistory.scrollTop = chatHistory.scrollHeight; // Auto-scroll to the bottom
}

sendMessageBtn.addEventListener('click', function() {
    const message = chatMessage.value.trim();
    if (message) {
        addMessageToChat(message, 'user');
        chatMessage.value = '';

        setTimeout(function() {
            const systemResponse = "Hello! How can I help you?";
            addMessageToChat(systemResponse, 'system');
        }, 500); // Add slight delay for system response
    }
});

//  Load File Content from GET Method and Display in Summary Area
document.addEventListener("DOMContentLoaded", function() {
    let polling = true;

    async function pollForFile() {
        try {
            const response = await fetch('https://api.beamhash.com/get-file');
            if (response.ok) {
                console.log("Getting the file content!!");
                const blob = response.blob;
                const reader = new FileReader();

                reader.onload = function(event) {
                    const fileContent = event.target.result;
                    console.log("Print the file content!!");
                    console.log(fileContent);

                    document.getElementById('audioSummary').innerText = fileContent;

                    polling = false; // Stop polling when the file is received
                    clearInterval(intervalId);
                };

                reader.readAsText(blob);
            } else {
                console.error('Failed to fetch file:', response.status);
            }
        } catch (error) {
            console.error('Error fetching file:', error);
        }
    }

    // Start polling every 5 seconds
    const intervalId = setInterval(pollForFile, 5000);
});





//----------------------------------------------------------------------------------
//  Load File Content from Event Stream and Display in Summary Area
//const audioSummary = document.getElementById('audioSummary');

//const eventSource = new EventSource('https://api.beamhash.com/events');

//eventSource.onmessage = function(event) {
//    const data = JSON.parse(event.data);
//    audioSummary.value = data.content; // Display content in the summary area
//};

// Close event source when the page is unloaded
//window.addEventListener('beforeunload', function() {
//    eventSource.close();
//})}
