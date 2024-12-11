// Login Logic
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

// Audio Recording & Upload Logic
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
            const audioBlob = new Blob(audioChunks, { type: 'audio/webm' });  // Change to 'audio/webm'
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

// Upload Audio with error handling
uploadBtn.addEventListener('click', async function() {
    if (!audioFile) {
        alert("No audio file available to upload");
        return;
    }

    const uniqueFilename = `recording_${Date.now()}.webm`;  // Ensure extension matches Blob type
    const formData = new FormData();
    formData.append('file', audioFile, uniqueFilename);

    try {
        const response = await fetch('https://api.beamhash.com/upload', {
            method: 'POST',
            body: formData,
            headers: {
                'Accept': 'application/json'
            }
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

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

// Chat Logic
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
    chatHistory.scrollTop = chatHistory.scrollHeight;
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

// Load File Content from Event Stream and Display in Summary Area
const audioSummary = document.getElementById('audioSummary');
const eventSource = new EventSource('https://api.beamhash.com/process-file');

eventSource.onmessage = function(event) {
    const data = JSON.parse(event.data);
    audioSummary.value = data.content;
};

// Close event source on unload
window.addEventListener('beforeunload', function() {
    eventSource.close();
});
