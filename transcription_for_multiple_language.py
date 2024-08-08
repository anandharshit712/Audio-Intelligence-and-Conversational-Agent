import datetime
import subprocess

import whisper
import torch
import pyannote.audio
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding
from pyannote.audio import Audio
from pyannote.core import Segment
import wave
import contextlib
from sklearn.cluster import AgglomerativeClustering
import numpy as np

embedding_model = PretrainedSpeakerEmbedding("speechbrain/spkrec-ecapa-voxceleb",
                                             device=torch.device("cuda" if torch.cuda.is_available() else "cpu"))

file_path = "audio1.wav"

num_speaker = 5  #@param {type: "integer"}
language = "any"  #@param ['any', 'English']
model_size = 'large'  #@param ['Tiny, 'Base', 'Smale', 'Medium', 'Large']

model_name = model_size
if language == 'English' and model_size != 'large':
    model_name += '.en'

if file_path[-3] != 'wav':
    subprocess.call(['ffmpeg', '-i', file_path, 'audio.wav', '-y'])
    file_path = 'audio.wav'

model = whisper.load_model(model_size)

result = model.transcribe(file_path)
segments = result["segments"]

with contextlib.closing(wave.open(file_path, 'r')) as f:
    frames = f.getnframes()
    rate = f.getframerate()
    duration = frames / float(rate)

audio = Audio()


def segment_embedding(segment):
    start = segment["start"]
    end = min(duration, segment["end"])
    clip = Segment(start, end)
    waveform, sample_rate = audio.crop(file_path, clip)
    return embedding_model(waveform[None])


embeddings = np.zeros(shape=(len(segments), 192))
for i, segment in enumerate(segments):
    embeddings[i] = segment_embedding(segment)

embeddings = np.nan_to_num(embeddings)

clustering = AgglomerativeClustering(num_speaker).fit(embeddings)
labels = clustering.labels_
for i in range(len(segments)):
    segments[i]["speaker"] = 'SPEAKER' + str(labels[i] + 1)


def time(secs):
    return datetime.timedelta(seconds=round(secs))

f = open("Transcript/Transcript_whisper_speaker.txt", "w")

for (i, segment) in enumerate(segments):
    if i == 0 or segments[i - 1]["speaker"] != segment["speaker"]:
        f.write("\n" + segment["speaker"] + '' + str(time(segment['start'])) + '\n')
    f.write(segment["text"][1:] + '')
f.close()