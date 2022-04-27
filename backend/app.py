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

# TODO Seperate File loc audio
UPLOAD_DIRECTORY = './tmp/'
TEMP_DIRECTORY = './temp/'

if not os.path.exists(UPLOAD_DIRECTORY):
    os.mkdir(UPLOAD_DIRECTORY)

app = Flask(__name__)


def audio_preprocessing(filename: str) -> list:
    """오디오 전처리"""
    file_path = webm_2_wav(filename=filename)

    xf, _ = librosa.load(path=file_path)
    mfcc_1 = librosa.feature.mfcc(y=xf, sr=16000, n_mfcc=5, n_fft=400, hop_length=160)
    mfcc_1 = scale(mfcc_1, axis=1)
    feature = np.mean(mfcc_1.T, axis=0)

    return [feature]


# TODO 파일을 저장하고 불러와서 다시 변환하고 삭제하는 형태이기에 저장장치에 무리를 줌
# TODO fs 모듈을 이용하여 해결하기를 권장
def webm_2_wav(filename: str) -> str:
    """WebM to Wav

    MediaEncoder에서 받으면 형식이 WebM 형식으로 받아짐.
    librosa에서 처리가 불가하므로 wav로 변환후 처리.

    Return: 
        str: filename
    """
    file_full: str = UPLOAD_DIRECTORY + filename
    audioSegment = AudioSegment.from_file(file_full)
    new_file_path = file_full.replace('webm', 'wav')
    audioSegment.export(new_file_path, format='wav')
    os.remove(file_full)

    return


def audio_predict(x) -> int:
    """결과값 예측"""
    result = MODEL.predict(x)

    return result[0].tolist()


# NOTE How about using `fs` save on ram and then convert?
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


# NOTE This page is not need
@app.route('/', methods=['GET'])
def hello() -> str:
    """Render html"""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
