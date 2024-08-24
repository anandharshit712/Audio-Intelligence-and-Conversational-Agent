import streamlit as st
import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import os

# Initialize session state variables if not already initialized
if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False
if 'audio_buffer' not in st.session_state:
    st.session_state.audio_buffer = []
if 'stream' not in st.session_state:
    st.session_state.stream = None
if 'sample_rate' not in st.session_state:
    st.session_state.sample_rate = 44100  # Standard CD-quality sample rate
if 'channels' not in st.session_state:
    st.session_state.channels = 2  # Stereo recording


def audio_callback(indata, frames, time, status):
    """
    This callback function is called for each audio block.
    It appends the incoming audio data to the session state's audio buffer.
    """
    if status:
        st.warning(f"Recording status: {status}")

    # Use Streamlit's experimental_rerun to safely modify session state in a separate thread
    with st.session_state_lock:
        if 'audio_buffer' in st.session_state:
            st.session_state.audio_buffer.append(indata.copy())
        else:
            st.session_state.audio_buffer = [indata.copy()]


def start_recording():
    """
    Starts the audio recording by opening an InputStream and setting the callback.
    """
    st.session_state.audio_buffer = []  # Reset the audio buffer
    st.session_state.stream = sd.InputStream(
        samplerate=st.session_state.sample_rate,
        channels=st.session_state.channels,
        callback=audio_callback
    )
    st.session_state.stream.start()
    st.session_state.is_recording = True
    st.success("Recording started... Click the button again to stop.")


def stop_recording():
    """
    Stops the audio recording, saves the recorded data to a .wav file,
    and resets the recording state.
    """
    if st.session_state.stream:
        st.session_state.stream.stop()
        st.session_state.stream.close()
        st.session_state.is_recording = False
        st.success("Recording stopped.")

        # Ensure there is recorded data to save
        if len(st.session_state.audio_buffer) > 0:
            # Concatenate all recorded audio blocks
            audio_data = np.concatenate(st.session_state.audio_buffer, axis=0)

            # Ensure the output directory exists
            folder_name = "recorded_audio"
            if not os.path.exists(folder_name):
                os.makedirs(folder_name)

            # Define the output file path
            file_name = "recording.wav"
            file_path = os.path.join(folder_name, file_name)

            # Save the recorded audio to a .wav file
            write(file_path, st.session_state.sample_rate, audio_data)
            st.info(f"Audio saved to `{file_path}`")
        else:
            st.warning("No audio data was recorded.")
    else:
        st.error("Recording was not started properly.")


# Streamlit App Layout
st.title("📢 Audio Recorder App")

st.write("Click the button below to start and stop recording your audio.")

# Lock for safe thread operation with session state
st.session_state_lock = st.empty()

# Button to start/stop recording
if st.button("Record" if not st.session_state.is_recording else "Stop Recording"):
    if not st.session_state.is_recording:
        start_recording()
    else:
        stop_recording()

# Optional: Display a message or instructions
if st.session_state.is_recording:
    st.write("🎤 Recording... Press the button again to stop.")
