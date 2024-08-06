import numpy as np
from pyAudioAnalysis import audioSegmentation as As
from pyAudioAnalysis import MidTermFeatures as mtf
from pyAudioAnalysis import audioBasicIO
from sklearn.mixture import GaussianMixture
import os
from joblib import parallel_backend

os.environ['OMP_NUM_THREADS'] = '4'


def speaker_count(file_path):
    max_speaker = 10
    mt_size = 2.0
    mt_step = 0.2
    st_win = 0.05
    st_step = 0.05

    [Fs, x] = audioBasicIO.read_audio_file(file_path)
    x = audioBasicIO.stereo_to_mono(x)

    result = mtf.mid_feature_extraction(x, Fs, mt_size * Fs, mt_step * Fs, round(Fs * st_win), round(Fs * st_step))

    # print("Returned result:", result)

    mt_feats = result[0]
    st_feat = result[1]

    mt_feats = np.transpose(mt_feats)

    mt_feats = (mt_feats - np.mean(mt_feats, axis = 0)) / np.std(mt_feats, axis = 0)

    bics = []
    with parallel_backend('threading', n_jobs=4):
        for n_speakers in range(1, max_speaker + 1):
            gmm = GaussianMixture(n_components=n_speakers, covariance_type='diag', n_init=1)
            gmm.fit(mt_feats)
            bic = gmm.bic(mt_feats)
            bics.append(bic)

    number_of_speaker = np.argmin(bics) + 1

    return number_of_speaker


file_path = "converted_audio.wav"
num_speaker = speaker_count(file_path)
print(f"Estimate Number of speakers in audio file are : {num_speaker}")

