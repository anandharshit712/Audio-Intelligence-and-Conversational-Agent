from langchain_community.llms.ollama import Ollama
import whisper
from detect_language import detect_language
from voice_isolation import voice_isolation
from noise_reduction import noise_reduction
from convert_to_wav import main
from ISO_to_name import iso_to_language_name
import assemblyai as aai
import torchaudio

ollama = Ollama(base_url = "http://localhost:11434", model = "mixtral:8x7b")
model = whisper.load_model('large')

def process_audio(file_path):
    file_path = "temp.wav"
    main(file_path)
    voice_isolation(file_path)
    noise_reduction(file_path)
    detected_language = detect_language(file_path)
    return detected_language

def load_audio(file_path):
    audio, sr = torchaudio.load(file_path)
    audio = audio.mean(dim=0)
    audio = torchaudio.transforms.Resample(orig_freq=sr, new_freq=16000)(audio)
    return audio

def whisper_transcript(file_path, language):
    if language:
        result = model.transcribe(file_path)
        transcription = result['text']
        return transcription

def create_transcript(file_path):
    file_path = "temp.wav"
    language = process_audio(file_path)
    language_name = iso_to_language_name(language)
    print(f"Audio Language: {language_name}")
    print("Creating transcript...")
    if language == "en":
        config = aai.TranscriptionConfig()
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(file_path, config=config)
        return transcript
    if language != "en":
        transcript = whisper_transcript(file_path, language)
        return transcript

# def translate(transcript, target_language):
