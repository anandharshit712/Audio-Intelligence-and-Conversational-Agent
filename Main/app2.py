import streamlit as st
import sounddevice as sd
import soundfile as sf
import tempfile

# Initialize chat history and audio file path
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "audio_file_path" not in st.session_state:
    st.session_state.audio_file_path = None

# Set up the Streamlit app
st.title("Audio-Interactive Chatbot")

# Function to record audio
def record_audio(duration, sample_rate):
    st.write("Recording...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=2, dtype='float32')
    sd.wait()  # Wait until recording is finished
    return audio

# Function to save audio to a temporary file
def save_audio(audio, sample_rate, file_path):
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    sf.write(temp_file.name, audio, sample_rate)

    sf.write(file_path, audio, sample_rate)
    return temp_file.name

# UI components for audio input
st.subheader("1. Record or Upload Audio")

# Audio recording section
duration = st.slider("Recording Duration (seconds)", min_value=1, max_value=60, value=5, step=1)
sample_rate = 44100  # Standard sample rate

if st.button('Record'):
    audio = record_audio(duration, sample_rate)
    st.session_state.audio_file_path = save_audio(audio, sample_rate, "Recorded_audio/recording1.wav")
    st.session_state.chat_history.append(("Audio recorded", "system"))

if uploaded_file := st.file_uploader("Or Upload an audio file", type=["wav", "mp3"]):
    st.session_state.audio_file_path = tempfile.NamedTemporaryFile(delete=False, suffix=".wav").name
    with open(st.session_state.audio_file_path, "wb") as f:
        f.write(uploaded_file.read())
    st.session_state.chat_history.append((f"Audio uploaded: {uploaded_file.name}", "system"))

# Display recorded audio
if st.session_state.audio_file_path:
    st.subheader("Recorded/Uploaded Audio")
    st.audio(st.session_state.audio_file_path, format="audio/wav")

# Display chat history
st.subheader("Ask Questions About the Audio")
for message, sender in st.session_state.chat_history:
    if sender == "user":
        st.write(f"You: {message}")
    else:
        st.write(f"System: {message}")

# Text input for questions
input_placeholder = st.empty()
user_input = input_placeholder.text_input(label=" ", placeholder="Ask a question about the audio:", key="question_input", value="")

if st.button("⬆", type="primary"):
    if user_input:
     # Simulate a response; replace this with actual audio processing logic
        response = f"Simulated response for the question: '{user_input}'"

            # Save to chat history
        st.session_state.chat_history.append((user_input, "user"))
        st.session_state.chat_history.append((response, "system"))

            # Clear the input field by resetting the value
        user_input = ""

        st.rerun()


st.markdown("""
    <style>
        .stTextInput div {
            position: fixed;
            bottom: 10px;
            width: 100%;
            max-width: 780px;
            left: 570px;
            height: 60px;
            border-radius: 50px;
            border: none;
        }
        .stTextInput input {
            padding-left: 20px;
            padding-bottom: 11px;
        }
        button[kind="primary"] {
            position: fixed;
            bottom: 20px;
            width: 100%;
            left: 1300px;
            max-width: 40px;
            border-radius: 25px;
            border: none;
            background-color: rgb(103, 103, 103);
        }
    </style>
""", unsafe_allow_html=True)