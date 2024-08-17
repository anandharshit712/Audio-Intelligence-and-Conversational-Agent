import assemblyai as aai
import collections
import moviepy.editor as mp
import noisereduce as nr
import librosa
import soundfile as sf
import mimetypes
import os
import numpy as np
from langchain_community.llms import Ollama
# from speaker_diarization import speaker_count
from sklearn.cluster import KMeans

aai.settings.api_key = "4da02acda77448cd8368d9d100fde23f"

ollama = Ollama(base_url="http://localhost:11434", model="mistral-nemo")


# Convert video file to audio
def video_to_audio(video_file):
    clip = mp.VideoFileClip(video_file)
    clip.audio.write_audiofile(r"audio.wav")


# Noise Reduction of audio file
def noise_reduction(audio_file):
    print("Removing Noise form the audio file...")
    audio_data, sample_rate = librosa.load(audio_file)
    reduced_noise = nr.reduce_noise(y=audio_data, sr=sample_rate)
    sf.write("clean_audio.wav", reduced_noise, sample_rate)
    print("Noise Reduction Complete")


# Create transcript and count number of speakers
def create_transcript(audio_file):
    print("Creating Transcript...")
    config = aai.TranscriptionConfig(speaker_labels=True)
    transcriber = aai.Transcriber()
    transcript = transcriber.transcribe(audio_file, config=config)
    speaker_count = collections.defaultdict(int)
    for utterance in transcript.utterances:
        speaker_count[utterance.speaker] += 1
    num_speaker = len(speaker_count)
    print(f"Number of speakers : ", num_speaker)
    speaker_label_map = {old_speaker: f"speaker{index + 1}" for index, old_speaker in enumerate(speaker_count.keys())}
    formatted_transcript = " "
    for utterance in transcript.utterances:
        speaker_name = speaker_label_map[utterance.speaker]
        formatted_transcript += f"{speaker_name} : {utterance.text}\n"

    return formatted_transcript


# Save transcript to text file
def save(transcript, file_name):
    with open(file_name, "w") as file:
        file.write(transcript)


# Process audio and create transcript
def process(path):
    mime_type, _ = mimetypes.guess_type(path)
    file_extension = os.path.splitext(path)[1].lower()
    if file_extension in ['.mp3', '.wav'] or mime_type in ['audio/mpeg', 'audio/wav']:
        noise_reduction(path)
    elif file_extension == 'mp4' or mime_type == 'video/mp4':
        video_to_audio(path)
        noise_reduction("audio.wav")

    transcript = create_transcript("clean_audio.wav")
    save(transcript, "Transcript/Transcript_test.txt")
    print("Transcript saved to Transcript2.txt...")

    prompt_input = input("Enter prompt for LLM:\n")
    prompt = transcript + prompt_input

    try:
        response = ollama(prompt)
    except Exception as e:
        print(f"Failed to get response from LLM model : {e}\nExiting....")
        return

    save(response, "Response/Response2_med_mistral-nemo_6.txt")
    print("Response saved to Response2.txt...")

    # while True:
    #     user_prompt = input("Enter your prompt (or type 'EXIT' to quit):")
    #     if user_prompt.upper() == "EXIT":
    #         print("Exiting...")
    #         break
    #
    #     prompt = f"{transcript}\n\n{user_prompt}"
    #
    #     try:
    #         response = ollama(prompt)
    #         # response_text = response["choices"][0]["text"]  # Assuming the response is in this format
    #         print("Response:\n", response)
    #     except Exception as e:
    #         print(f"Failed to get response from LLM model : {e}\nExiting....")
    #         break

# path_to_file = "Test audio/Cardiac_Arrest.mp3"
path_to_file = "clean_audio.wav"
process(path_to_file)

