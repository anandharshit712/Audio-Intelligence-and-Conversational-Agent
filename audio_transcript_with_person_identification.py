import assemblyai as aai
import collections
import moviepy.editor as mp
import noisereduce as nr
import librosa
import soundfile as sf
from langchain_community.llms import Ollama


aai.settings.api_key = "4da02acda77448cd8368d9d100fde23f"

# Convert video file to audio
clip = mp.VideoFileClip(r"ANI2.mp4")
clip.audio.write_audiofile(r"audio.wav")


# Noise Reduction in the converted audio file
print("Removing Noise form the Audio file...")
audio_data, sample_rate = librosa.load("audio.wav")
reduced_noise = nr.reduce_noise(y=audio_data, sr=sample_rate)
sf.write("cleaned_audio.wav", reduced_noise, sample_rate)
print("Noise Reduction Complete...")


print("Creating Transcript...")
PATH = "cleaned_audio.wav"

config = aai.TranscriptionConfig(speaker_labels=True)

transcriber = aai.Transcriber()
transcript = transcriber.transcribe(PATH, config=config)

# Initialize a dictionary to count occurrences of each speaker
speaker_counts = collections.defaultdict(int)

# Populate the dictionary with speaker occurrences
for utterance in transcript.utterances:
    speaker_counts[utterance.speaker] += 1

# Get the number of unique speakers
num_speakers = len(speaker_counts)
print(f"Number of unique speakers: {num_speakers}")

# Prepare the formatted transcript with dynamic speaker labels
speaker_label_map = {old_speaker: f"speaker{index + 1}" for index, old_speaker in enumerate(speaker_counts.keys())}
formatted_transcript = ""

# Generate speaker-labeled transcript
for utterance in transcript.utterances:
    speaker_name = speaker_label_map[utterance.speaker]
    formatted_transcript += f"{speaker_name}: {utterance.text}\n"


# Save transcript to a text file
with open("Transcript.txt", "w") as file:
    file.write(formatted_transcript)

print("Transcript saved to Transcript.txt")

print("Transcript sent to LLM model.\nWaiting for response...")

ollama = Ollama(base_url="http://localhost:11434", model="llama3")

prompt = "Summarize the following content:\n\n" + formatted_transcript

try:
    responses = ollama(prompt)
    with open("Response.txt", "w") as file:
        file.write(responses)
except Exception as e:
    print(f"Failed to get response from LLM model : {e}\nExiting....")

print("LLM response saved to Response.txt")
