from transformers import WhisperTokenizer, WhisperForConditionalGeneration, WhisperFeatureExtractor
import soundfile as sf
import torch

# Define the path to your audio file
audio_file_path = "CallRecording3.mp3"

# Convert audio file to the correct format (16-bit PCM WAV, mono channel, 16000 Hz sample rate)
from pydub import AudioSegment
audio = AudioSegment.from_file(audio_file_path)
audio = audio.set_frame_rate(16000).set_channels(1).set_sample_width(2)
audio.export("converted_audio.wav", format="wav")

# Load the audio file
audio_data, _ = sf.read("converted_audio.wav")

# Load the Whisper model, tokenizer, and feature extractor
model_name = "openai/whisper-large-v3"
feature_extractor = WhisperFeatureExtractor.from_pretrained(model_name)
tokenizer = WhisperTokenizer.from_pretrained(model_name)
model = WhisperForConditionalGeneration.from_pretrained(model_name)

# Prepare the input features
inputs = feature_extractor(audio_data, return_tensors="pt", sampling_rate=16000)
input_features = inputs.input_features

# Generate the transcription
with torch.no_grad():
    # Ensure the input_features are on the same device as the model
    input_features = input_features.to(model.device)
    predicted_ids = model.generate(input_features)  # Specify language for translation to English

# Decode the generated ids to text
transcript = tokenizer.batch_decode(predicted_ids, skip_special_tokens=True)

# Print the results
print(f"Transcript: {transcript}")
