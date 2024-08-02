import whisper
import torchaudio
import torch
import os

model_name = "medium"
local_model_path = f"{model_name}.pt"

# Function to load and preprocess the audio file
def load_audio(file_path):
    audio, sr = torchaudio.load(file_path)
    audio = audio.mean(dim=0)  # Convert to mono
    resampler = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)
    audio = resampler(audio)  # Resample to 16kHz
    return audio

# Load the Whisper model
if not os.path.exists(local_model_path):
    model = whisper.load_model(model_name)
    torch.save(model.state_dict(), local_model_path)
else:
    model = whisper.load_model(model_name)
    model.load_state_dict(torch.load(local_model_path, map_location=torch.device('cpu')))

# Ensure the model is in evaluation mode
model.eval()

# Load the audio file
audio = load_audio("CallRecording3.mp3")

# Pad or trim audio to fit Whisper's expected input length
audio = whisper.pad_or_trim(audio)

# Make log-Mel spectrogram and move to the same device as the model
mel = whisper.log_mel_spectrogram(audio.unsqueeze(0)).to(model.device)

# Detect the spoken language
options = whisper.DecodingOptions(task="language", without_timestamps=True)
result = whisper.decode(model, mel, options)
detected_language = result.language
print(f"Detected language: {detected_language}")

# Transcribe the audio
result = model.transcribe("path_to_your_audio_file.mp3")
transcription = result["text"]
print("Transcription:", transcription)

# Save the transcription to a text file
with open("transcription.txt", "w", encoding="utf-8") as f:
    f.write(transcription)

# If the detected language is not English, translate the transcription
if detected_language != "en":
    translated = model.transcribe("path_to_your_audio_file.mp3", task="translate")
    translation = translated["text"]
    print("Translation:", translation)

    # Save the translation to a text file
    with open("translation.txt", "w", encoding="utf-8") as f:
        f.write(translation)
