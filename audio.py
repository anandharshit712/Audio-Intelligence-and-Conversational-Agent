import whisper
import torch
import os
import numpy as np
from pydub import AudioSegment
from tempfile import TemporaryDirectory


def load_audio(file_path, sample_rate=16000):
    audio = AudioSegment.from_file(file_path)
    audio = audio.set_frame_rate(sample_rate).set_channels(1)
    audio_array = np.array(audio.get_array_of_samples())
    return torch.tensor(audio_array, dtype=torch.float32) / 32768.0


def transcribe_audio(model, audio, chunk_size=30, language=None):
    duration = len(audio) / 16000  # since the sample rate is 16kHz
    if duration <= chunk_size:
        return model.transcribe(audio, language=language)["text"]

    transcript = []
    with TemporaryDirectory() as tmpdir:
        for i in range(0, int(duration), chunk_size):
            chunk_audio = audio[i * 16000:(i + chunk_size) * 16000]
            chunk_path = os.path.join(tmpdir, f"chunk_{i}.wav")
            chunk_audio = AudioSegment(
                chunk_audio.numpy().astype(np.float32),
                frame_rate=16000,
                sample_width=2,
                channels=1
            )
            chunk_audio.export(chunk_path, format="wav")
            result = model.transcribe(chunk_path, language=language)
            transcript.append(result["text"])

    return " ".join(transcript)


def main(audio_path, model_size="medium", language=None):
    # Load Whisper model
    model = whisper.load_model(model_size)

    # Load audio file
    audio = load_audio(audio_path)

    # Transcribe the audio
    transcription = transcribe_audio(model, audio, language=language)

    # Print transcription
    print("Transcription:")
    print(transcription)


if __name__ == "__main__":
    audio_path = "audio.wav"  # Replace with your audio file path
    language = None  # Specify the language code if known, e.g., 'en' for English
    main(audio_path, language=language)
