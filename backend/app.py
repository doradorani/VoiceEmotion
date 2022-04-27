import os
import warnings

import joblib
import librosa
import numpy as np
from flask import Flask, jsonify, render_template, request
from flask.wrappers import Response
from sklearn.preprocessing import scale
from werkzeug.utils import secure_filename
from pydub import AudioSegment

warnings.filterwarnings('ignore')

MODEL = joblib.load(open('../model/saved_model/model_lgbm.pkl', 'rb'))
Label = ['anger', 'angry', 'disgust', 'fear', 'happiness', 'neutral', 'sad', 'surprise']
UPLOAD_DIRECTORY = './tmp/'

if not os.path.exists(UPLOAD_DIRECTORY):
    os.mkdir(UPLOAD_DIRECTORY)

app = Flask(__name__)


def audio_preprocessing(filename) -> list:
    """오디오 전처리"""
    file_full: str = UPLOAD_DIRECTORY + filename
    audioSegment = AudioSegment.from_file(file_full)
    new_file_path = file_full.replace('webm', 'wav')
    audioSegment.export(new_file_path, format='wav')
    xf, _ = librosa.load(file_full)
    mfcc_1 = librosa.feature.mfcc(y=xf, sr=16000, n_mfcc=5, n_fft=400, hop_length=160)
    mfcc_1 = scale(mfcc_1, axis=1)
    feature = np.mean(mfcc_1.T, axis=0)

    return [feature]


def webm_2_wav() -> None:  # TODO
    pass


def audio_predict(x) -> int:
    """결과값 예측"""
    result = MODEL.predict(x)

    return result[0].tolist()


@app.route('/receive', methods=['POST'])
def form() -> Response:
    """Get wav file"""
    file = request.files['file']
    if file.filename is not None:
        filename = secure_filename(filename=file.filename)
        file.save(os.path.join(UPLOAD_DIRECTORY, filename))
        _x_val = audio_preprocessing(file.filename)
        predict_result = audio_predict(_x_val)

        return jsonify({'status': 'success', 'result': Label[predict_result]})
    else:
        return jsonify({'status': 'fail'})


@app.route('/', methods=['GET'])
def hello() -> str:
    """Render html"""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
