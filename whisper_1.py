import whisper

model = whisper.load_model('large')

def transcribe(audio_file, detected_language):
    if detected_language:
        result = model.transcribe("temp.wav")
        transcription = result['text']
        return transcription
    else:
        print("Language detection failed; skipping transcription and translation.")
        return None

print(transcribe("temp.wav", "en"))