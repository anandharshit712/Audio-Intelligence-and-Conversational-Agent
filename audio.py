import whisper
from pydub import AudioSegment
from pydub.silence import split_on_silence

# Load the Whisper model
model = whisper.load_model("medium")  # You can choose "small", "medium", or "large" as well


# Function to transcribe audio and detect speakers
def transcribe_and_detect_speakers(audio_path):
    # Load and convert the audio file
    audio = AudioSegment.from_file(audio_path)

    # Split the audio into chunks based on silence
    chunks = split_on_silence(audio, silence_thresh=-20)  # Adjust silence threshold as needed

    # Process each chunk with Whisper
    transcripts = []
    for i, chunk in enumerate(chunks):
        chunk.export("temp.wav", format="wav")
        result = model.transcribe("temp.wav", language=None)  # Specify the language or leave as None for auto-detection
        speaker_name = f"Speaker{i + 1}"  # Assign a name like "Speaker1", "Speaker2", etc.
        transcripts.append(f"{speaker_name}: {result['text']}")

    # Combine the transcripts
    full_transcript = "\n".join(transcripts)

    # Count speakers
    num_speakers = len(chunks)

    return full_transcript, num_speakers


# Example usage
audio_path = "audio.wav"
transcript, speakers = transcribe_and_detect_speakers(audio_path)
print("Transcript:\n", transcript)
print("Number of Speakers:", speakers)
