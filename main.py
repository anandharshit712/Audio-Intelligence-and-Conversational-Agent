from langchain_community.llms.ollama import Ollama
import whisper
from detect_language import detect_language
from voice_isolation import voice_isolation
from noise_reduction import noise_reduction
from translation import translate_file
from convert_to_wav import convert
from ISO_to_name import iso_to_language_name
import assemblyai as aai

ollama = Ollama(base_url = "http://localhost:11434", model = "mistral-nemo")
model = whisper.load_model('large')

def language_detection(file_path):
    detected_language = detect_language(file_path)
    return detected_language

def process_audio(file_path):
    file_path = "temp.wav"
    convert(file_path)
    voice_isolation(file_path)
    noise_reduction(file_path)

def whisper_transcript(file_path, language):
    if language:
        result = model.transcribe(file_path)
        transcription = result['text']
        return transcription

def translate(file, target_language):
    if target_language == "en":
        translated_text = translate_file(file, target_language)
        return translated_text
    else:
        response_translation = translate_file(file, target_language)
        return response_translation

def create_transcript(file_path):
    file_path = "temp.wav"
    language = language_detection(file_path)
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

def LLM(transcript, question):
    prompt = transcript + question
    try:
        response = ollama(prompt)
    except Exception as e:
        print(f"Failed to get response from LLM model : {e}\nExiting....")
        return
    return response

def save_files(content, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("File Saved Successfully")

def main():
    path = "Test audio/CallRecording3.mp3"
    original_language = language_detection(path)
    process_audio(path)
    transcript = create_transcript("temp.wav")
    save_files(transcript, "Transcript_main/transcript_main.txt")
    if original_language != "en":
        eng_transcript = translate(transcript, "en")
        save_files(eng_transcript, "Transcript_main/Transcript_main_eng/eng_transcript_main1.txt")
    query = input("Enter Prompt!!!")
    LLM_response = LLM(eng_transcript, query)
    save_files(LLM_response, "Response_main/Response_main_eng/eng_response_main.txt")
    ori_lang_response = translate(LLM_response, original_language)
    save_files(ori_lang_response, "Response_main/Response_main/ori_response_main.txt")

if __name__ == "__main__":
    main()
