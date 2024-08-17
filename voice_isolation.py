import librosa
import numpy as np
import soundfile as sf

# Load audio file
audio_path = 'cleaned_audio.wav'
y, sr = librosa.load(audio_path, sr=None)

# Short-time Fourier transform (STFT)
stft = librosa.stft(y)

# Magnitude and phase
magnitude, phase = np.abs(stft), np.angle(stft)

# Create a noise profile
# This could be based on a segment of the audio where there's no speech
noise_profile = np.mean(magnitude[:, :int(sr*0.5)], axis=1)

# Estimate a mask where the magnitude is above the noise threshold
noise_threshold = 1.5 * noise_profile
mask = magnitude > noise_threshold[:, np.newaxis]

# Apply mask to the STFT
isolated_stft = stft * mask

# Inverse STFT to get back to time domain
isolated_audio = librosa.istft(isolated_stft)

# Save the isolated audio
sf.write('isolated_audio.wav', isolated_audio, sr)
