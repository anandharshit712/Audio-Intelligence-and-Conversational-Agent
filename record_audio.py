import sounddevice as sd
import numpy as np
from scipy.io.wavfile import write
import os
import threading

def Record():
    # Parameters
    sample_rate = 44100  # Sample rate in Hz
    folder_name = "recorded_audio"
    file_name = "recording.wav"
    recording = None
    is_recording = True

    # Ensure the output folder exists
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    def record_audio():
        nonlocal recording, is_recording
        print("Recording... Press Enter to stop.")
        recording = sd.rec(frames=int(sample_rate * 3600), samplerate=sample_rate, channels=2, dtype='float64')
        sd.wait()  # Wait until recording is finished or manually stopped
        is_recording = False
        print("Recording stopped.")

    def stop_recording():
        nonlocal is_recording
        input()  # Wait for user input (Enter key)
        sd.stop()  # Stop the recording
        is_recording = False

    # Start recording in a separate thread
    recording_thread = threading.Thread(target=record_audio)
    recording_thread.start()

    # Start a separate thread to listen for the Enter key
    stop_thread = threading.Thread(target=stop_recording)
    stop_thread.start()

    # Wait for the recording thread to finish
    recording_thread.join()

    # Save the recording if it was started
    if recording is not None:
        recording = recording[:np.sum(np.abs(recording) > 0)]  # Trim the silent part
        file_path = os.path.join(folder_name, file_name)
        write(file_path, sample_rate, recording)
        print(f"Audio saved to {file_path}")
    else:
        print("No recording was made.")

# To start recording, simply call the Record function
Record()
