import os
import warnings
import pandas as pd
import joblib
import librosa
import numpy as np
from flask_cors import CORS
from flask import Flask, jsonify, render_template, request, url_for, redirect, session, escape
from flask.wrappers import Response
from sklearn.preprocessing import scale
from werkzeug.utils import secure_filename
from pydub import AudioSegment
from pathlib import Path
warnings.filterwarnings('ignore')
import pymysql 
from sklearn.metrics.pairwise import cosine_similarity
import io
from google.cloud import speech

# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/User/Downloads/aivlebigproject-348610-27ad2f7a9168.json"
BASE_DIR = Path(__file__).resolve().parent.parent

# ----------------------------------------------------------------------------------------------------------------------------------

# ---사용자 정의 함수-----------------------------------------------------------------------------------------------------------------
def audio_preprocessing(filename: str) -> list:
    """오디오 전처리"""
    file_full = UPLOAD_DIRECTORY + filename
    audioSegment = AudioSegment.from_file(file_full)
    audioSegment = audioSegment.set_sample_width(sample_width=2)
    new_file_path = file_full.replace('webm', 'wav')
    audioSegment.export(new_file_path, format='wav', bitrate = '16k')
    return [new_file_path]

UPLOAD_DIRECTORY = './tmp/'
TEMP_DIRECTORY = './temp/'

if not os.path.exists(UPLOAD_DIRECTORY):
    os.mkdir(UPLOAD_DIRECTORY)

app = Flask(__name__)
CORS(app=app, resources={r'*': {'origins': '*'}})

# NOTE How about using `fs` save on ram and then convert?
@app.route('/receive', methods=['POST'])
def emotion() -> Response:
    """Get wav file"""
    file = request.files['file']

    if file.filename is not None:
        filename = secure_filename(filename=file.filename)
        file.save(os.path.join(UPLOAD_DIRECTORY, filename))
        new_file_path = audio_preprocessing(file.filename)
        print("new_file_path", new_file_path)
        print("file.filename", file.filename)
        return jsonify({'status': 'success'})
    else:
        return jsonify({'status': 'fail'})

# NOTE This page is not need
@app.route('/', methods=['GET'])
def hello() -> str:
    """Render html"""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
