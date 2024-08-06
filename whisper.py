import whisper
import torchaudio
import torch

# Load whisper model
model = whisper.load_model('medium')


def load_audio(file_path):
    audio, sr = torchaudio.load(file_path)
    audio = audio.mean(dim=0)
    audio = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)(audio)
    return audio


audio = load_audio("CallRecording3.mp3")

# Pad or trim the audio
audio_padded = whisper.pad_or_trim(audio)

# Convert the audio to mel spectrogram
mel = whisper.log_mel_spectrogram(audio_padded.unsqueeze(0)).to(model.device)

# Detect Language
lang_result = model.detect_language(mel)

# Debug print to inspect the structure of lang_result
print(f"lang_result: {lang_result}")

# Store all elements except the first one in another variable
probs = lang_result[1] if len(lang_result) > 1 else []

# Ensure probs is a dictionary
if isinstance(probs, list) and len(probs) > 0 and isinstance(probs[0], dict):
    probs = probs[0]
    detected_language = max(probs, key=probs.get)
    print(f"Detected Language: {detected_language}")
else:
    print("Error: 'probs' is not a dictionary")
    detected_language = None

# Proceed with transcription and translation only if language detection succeeded
if detected_language:
    # Transcribe the audio
    result = model.transcribe("CallRecording3.mp3")
    transcription = result['text']
    print("Transcription:", transcription)

    # Save the transcript to text file
    with open("transcription.txt", "w", encoding="utf-8") as f:
        f.write(transcription)

    # If the detected language is not English, translate the transcription
    if detected_language != "en":
        translated = model.transcribe("CallRecording3.mp3", task="translate")
        translation = translated["text"]
        print("Translation:", translation)

        with open("translation.txt", "w", encoding="utf-8") as f:
            f.write(translation)
else:
    print("Language detection failed; skipping transcription and translation.")
