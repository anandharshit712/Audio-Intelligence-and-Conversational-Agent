import whisper
import torchaudio

model = whisper.load_model('large')

def load_audio(audio_path):
    audio, sr = torchaudio.load(audio_path)
    audio = audio.mean(dim=0)
    audio = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)(audio)
    return audio

def detect_language(audio_path):
    audio = load_audio(audio_path)
    audio_padded = whisper.pad_or_trim(audio)
    mel = whisper.log_mel_spectrogram(audio_padded.unsqueeze(0), n_mels=128).to(model.device)
    lang_result = model.detect_language(mel)
    probs = lang_result[1] if len(lang_result) > 1 else []

    if isinstance(probs, list) and len(probs) > 0 and isinstance(probs[0], dict):
        probs = probs[0]
        detected_language = max(probs, key=probs.get)
    else:
        detected_language = None

    # print(detected_language)
    return detected_language

# file_path = "Test audio/CallRecording2.mp3"
# language = detect_language(file_path)
# print(language)