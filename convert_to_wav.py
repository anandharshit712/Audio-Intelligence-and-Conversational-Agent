import moviepy.editor as mp
from pydub import AudioSegment
import librosa
import noisereduce as nr
import soundfile as sf
import mimetypes
import os

def video_to_wav(file_path):
    clip = mp.VideoFileClip(file_path)
    clip.audio.write_audiofile(r"temp.wav")

def mp3_to_wav(file_path):
    output_file = "temp.wav"
    sound = AudioSegment.from_mp3(file_path)
    sound.export(output_file, "wav")

def convert(path):
    mime_type, _ = mimetypes.guess_type(path)
    file_extension = os.path.splitext(path)[1].lower()
    if file_extension == ".mp3" or mime_type == "audio/mpeg":
        mp3_to_wav(path)
    elif file_extension == ".mp4" or mime_type == "video/mp4":
        video_to_wav(path)

# if __name__ == '__main__':
#     path = "Test audio/CallRecording3.mp3"
#     # path = "Test videos/Breast_Cancer.mp4"
#     main(path)