from transformers import pipeline, AutoModelForSpeechSeq2Seq, AutoProcessor
from huggingface_hub import login
from pydub import AudioSegment
import soundfile as sf
import torch

# Define your Hugging Face API key
API_KEY = "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"

# Log in to Hugging Face Hub
login(API_KEY)

# Load the model and processor directly
model = AutoModelForSpeechSeq2Seq.from_pretrained("openai/whisper-large-v2")
processor = AutoProcessor.from_pretrained("openai/whisper-large-v2")

# Initialize the pipeline
transcription_pipeline = pipeline(
    task="automatic-speech-recognition",
    model=model,
    # processor=processor,
    feature_extractor=processor.feature_extractor,
    tokenizer=processor.tokenizer,
    framework="pt"
)

# Path to your audio file
audio_file_path = "CallRecording3.mp3"

# Convert audio file to the correct format (16-bit PCM WAV, mono channel, 16000 Hz sample rate)
audio = AudioSegment.from_file(audio_file_path)
audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
audio.export("converted_audio.wav", format="wav")

# Read the converted audio file
audio_data, _ = sf.read("converted_audio.wav")

# Process the audio file
inputs = processor(audio_data, sampling_rate=16000, return_tensors="pt", padding=True)
input_features = inputs.input_features

# Check if attention_mask is present and use it if available
if "attention_mask" in inputs:
    attention_mask = inputs.attention_mask
    with torch.no_grad():
        predicted_ids = model.generate(input_features, attention_mask=attention_mask)
else:
    with torch.no_grad():
        predicted_ids = model.generate(input_features)

# Decode the predicted IDs to text
transcript = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]

# Print the results
print(f"Transcript: {transcript}")
