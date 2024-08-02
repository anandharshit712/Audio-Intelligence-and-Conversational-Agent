import assemblyai as aai
import nltk
import requests
import time
from nltk.tokenize import sent_tokenize

nltk.download('punkt')
# Replace with your API key
aai.settings.api_key = "4da02acda77448cd8368d9d100fde23f"

# Path to your local audio file
PATH = "Locked_Away.mp3"


# Upload the audio file to AssemblyAI
def upload_file(file_path):
    headers = {
        "authorization": aai.settings.api_key
    }
    with open(file_path, "rb") as f:
        response = requests.post("https://api.assemblyai.com/v2/upload", headers=headers, files={"file": f})
    response.raise_for_status()
    return response.json()["upload_url"]


# Request transcription
def request_transcription(audio_url):
    headers = {
        "authorization": aai.settings.api_key,
        "content-type": "application/json"
    }
    data = {
        "audio_url": audio_url
    }
    response = requests.post("https://api.assemblyai.com/v2/transcript", json=data, headers=headers)
    response.raise_for_status()
    return response.json()["id"]


# Check transcription status
def check_transcription_status(transcription_id):
    headers = {
        "authorization": aai.settings.api_key
    }
    response = requests.get(f"https://api.assemblyai.com/v2/transcript/{transcription_id}", headers=headers)
    response.raise_for_status()
    return response.json()


# Transcribe the audio file
def transcribe_file(file_path):
    # Upload the file
    audio_url = upload_file(file_path)
    print(f"Uploaded audio file to URL: {audio_url}")

    # Request transcription
    transcription_id = request_transcription(audio_url)
    print(f"Requested transcription with ID: {transcription_id}")

    # Poll for transcription result
    while True:
        result = check_transcription_status(transcription_id)
        if result["status"] == "completed":
            return result["text"]
        elif result["status"] == "failed":
            raise Exception("Transcription failed")
        print("Waiting for transcription to complete...")
        time.sleep(5)


# Run the transcription
try:
    transcription_text = transcribe_file(PATH)
    print("Transcription: " + transcription_text)

    sentences = sent_tokenize(transcription_text)

    # Join sentences into paragraphs
    paragraph_length = 5  # Adjust the number of sentences per paragraph
    paragraphs = [' '.join(sentences[i:i + paragraph_length]) for i in range(0, len(sentences), paragraph_length)]
    formatted_text = '\n\n'.join(paragraphs)


    # Save the transcription to a text file
    with open("transcription.txt", "w") as file:
        file.write(formatted_text)
    print("Transcription saved to transcription.txt")
except Exception as e:
    print(f"Error: {e}")
