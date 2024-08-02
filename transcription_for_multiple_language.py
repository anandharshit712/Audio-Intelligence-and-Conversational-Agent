import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
# import os
from pydub import AudioSegment
from langchain_community.llms import Ollama
import noisereduce as nr
import librosa
import soundfile as sf


# Read text files
def read_text_file(file_path):
    try:
        with open(file_path, 'r', encoding = 'utf-8') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File at {file_path} was not found!!!")
        return None
    except Exception as e:
        print(f"Error during reading file at {file_path} : {e}")
        return None


# Write to a text file
def write_text_file(file_path, content):
    try:
        with open(file_path, 'w', encoding = 'utf-8') as file:
            file.write(content)
    except Exception as e:
        print(f"Error writing file at {file_path} : {e}")


# Initialize model with localhost
ollama = Ollama(base_url = "http://localhost:11434", model = "llama3")


# Speech to text
def speech_to_text(audio_file_path, language):
    recognizer = sr.Recognizer()
    audio = AudioSegment.from_file(audio_file_path)
    audio.export('temp.wav', format = 'wav')
    with sr.AudioFile("temp.wav") as source:
        audio_data = recognizer.record(source)
        try:
            text = recognizer.recognize_google(audio_data, language = language)
            print(f"Transcribed text : {text}")
            return text
        except sr.UnknownValueError:
            print(f"Google Speech Recognition cannot understand the audio")
            return None
        except sr.RequestError as e:
            print(f"Could not request from Google Speech Recognition service: {e}")
            return None
        # finally:
        #     os.remove("temp.wav")


# Translate text to english
def translate_text(text, target_language = 'en'):
    translator = Translator()
    try:
        translated = translator.translate(text, dest = target_language)
        return translated.text
    except Exception as e:
        print(f"Translation Error: {e}")
        return None


# Text to Speech
def text_to_speech(text, language = 'en'):
    try:
        tts = gTTS(text = text, lang = language)
        tts.save("output.mp3")
    except Exception as e:
        print(f"TTS error : {e}")


# Main audio processing function
def process_audio_file(audio_file_path, original_language, target_language = 'en'):
    # Convert speech to text
    transcribed_text = speech_to_text(audio_file_path, language = original_language)
    if transcribed_text is None:
        print("Failed to transcribe audio fle.\nExiting...")
        return

    # translate transcribed text to english
    translated_text = translate_text(transcribed_text, target_language)
    if translated_text is None:
        print("Failed to translate the transcribed text.\nExiting...")
        return

    # Summarization prompt
    prompt = "Summerize the following conten:\n\n" + translated_text

    # use prompt to get the result from the model
    try:
        response = ollama(prompt)
    except Exception as e:
        print(f"Failed to get response from the model: {e}\nExiting...")
        return

    # translate to model's response back to the original language
    final_translated_text = translated_text(response, target_language = original_language)
    if final_translated_text is None:
        print("Failed to translate model's response.\nExiting...")
        return

    # write the original transcript, final translated model's response to text files
    response_file_path = 'response.txt'
    write_text_file(response_file_path, response)
    transcript_file_path = 'transcript.txt'
    write_text_file(transcript_file_path, transcribed_text)
    print(f"Transcript written to {transcript_file_path}\nResponse written to {response_file_path}")


audio_file_path = 'CallRecording1.mp3'
original_language = 'hi'
print("Removing Noise form the Audio file...")
audio_data, sample_rate = librosa.load(audio_file_path)
reduced_noise = nr.reduce_noise(y=audio_data, sr=sample_rate)
sf.write("cleaned_audio.wav", reduced_noise, sample_rate)
print("Noise Reduction Complete...")
process_audio_file('cleaned_audio.wav', original_language)