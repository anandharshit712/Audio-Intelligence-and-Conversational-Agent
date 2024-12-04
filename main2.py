import os, time
from langchain_community.llms.ollama import Ollama
from language_detect_test import detect_lang
from noise_reduction import noise_reduction
from translation import translate_file
from convert_to_wav import convert
from ISO_to_name import iso_to_language_name
from whisper_1 import transcribe
import assemblyai as aai

aai.settings.api_key = "4da02acda77448cd8368d9d100fde23f"
ollama = Ollama(base_url="http://localhost:11434", model="llama3.1")

def language_detection(file_path):
    detected_language = detect_lang(file_path)
    return detected_language

def process_audio(file_path):
    convert(file_path)
    noise_reduction("temp.wav")

def whisper_transcript(file_path, language):
    transcript = transcribe(file_path, language)
    return transcript

def translate(file, target_language):
    translated_text = translate_file(file, target_language)
    return translated_text

def create_transcript(file_path):
    language = language_detection(file_path)
    language_name = iso_to_language_name(language)
    print(f"Audio Language: {language_name}")
    print("Creating transcript...")
    if language == "en":
        config = aai.TranscriptionConfig()
        transcriber = aai.Transcriber()
        transcript = transcriber.transcribe(file_path, config=config)
        return transcript.text
    if language != "en":
        transcript = whisper_transcript(file_path, language)
        return transcript

def LLM(transcript, question):
    prompt = transcript + question
    try:
        response = ollama(prompt)
        return response
    except Exception as e:
        print(f"Failed to get response from LLM model: {e}/nExiting....")
        return

def save_files(content, file_path):
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print("File Saved Successfully")

def main():
    path = "Audio/Thalaseemia.mp3"
    response_path = "Output_data/Response/"
    transcript_path = "Output_data/Transcript"
    audio_file_name = os.path.splitext(os.path.basename(path))[0]
    original_language = language_detection(path)
    process_audio(path)
    transcript = create_transcript("temp.wav")
    if original_language == "en":
        eng_transcript = transcript
        save_files(eng_transcript, os.path.join(transcript_path+"/English", f"{audio_file_name}_eng.txt"))
    else:
        save_files(transcript, os.path.join(transcript_path+"/Original_language", f"{audio_file_name}_ori.txt"))
        eng_transcript = translate(os.path.join(transcript_path+"/Original_language", f"{audio_file_name}_ori.txt"), "en")
        save_files(eng_transcript, os.path.join(transcript_path+"/English", f"{audio_file_name}_eng.txt"))
    # query = input("Enter Prompt!!! ")
    # query = "Explain about the issue mentioned in the conversation and the ways to reduce the same."
    query = "Summarize"
    LLM_response = LLM(eng_transcript, query)
    print("Getting LLM Response...")
    save_files(LLM_response, os.path.join(response_path+"/English", f"{audio_file_name}_eng.txt"))
    if original_language != "en":
        ori_lang_response = translate(os.path.join(response_path+"/English", f"{audio_file_name}_eng.txt"), original_language)
        save_files(ori_lang_response, os.path.join(response_path+"/Original_language", f"{audio_file_name}_ori.txt"))
if __name__ == "__main__":
    st = time.time()
    main()
    et = time.time()
    execution_time = et - st
    print(f"Execution time: {execution_time:.6f} seconds")
