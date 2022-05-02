import os
import warnings
import pandas as pd
import joblib
import librosa
import numpy as np
from flask_cors import CORS
from flask import Flask, jsonify, render_template, request, url_for, redirect
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

os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/User/Downloads/aivlebigproject-348610-27ad2f7a9168.json"
BASE_DIR = Path(__file__).resolve().parent.parent

# ---data 불러오기------------------------------------------------------------------------------------------------------------------
db = pymysql.connect(user = 'root', host = '192.18.138.86', passwd = '5631jjyy', port = 3306, db = 'jango_db')
cursor = db.cursor(pymysql.cursors.DictCursor)
sql = "SELECT * FROM movie"
cursor.execute(sql)
movie_df = pd.DataFrame(data=cursor.fetchall(), columns=['movieId', 'title', 'genres'])
cursor = db.cursor(pymysql.cursors.DictCursor)
sql = "SELECT * FROM ratings"
cursor.execute(sql)
ratings_df = pd.DataFrame(data=cursor.fetchall(), columns=['idx', 'userId', 'movieId', 'rating', 'ts'])
movie_df_copy = movie_df.copy()
# ----------------------------------------------------------------------------------------------------------------------------------

# ---model 불러오기------------------------------------------------------------------------------------------------------------------
MODEL = joblib.load(open(os.path.join(BASE_DIR,'model/saved_model/model_lgbm.pkl'), 'rb'))
Label = ['anger', 'angry', 'disgust', 'fear', 'happiness', 'neutral', 'sad', 'surprise']
# ----------------------------------------------------------------------------------------------------------------------------------

# ---사용자 정의 함수-----------------------------------------------------------------------------------------------------------------

def stt(file_name):
    """stt 변환해서 제대로 말했는지 확인"""
    # 클라이언트 인스턴스화
    client = speech.SpeechClient()
    
    # # 오디오 파일 이름
    # file_name = UPLOAD_DIRECTORY + filename
    # 오디오 파일 불러오기
    with io.open(file_name, 'rb') as audio_file:
        content = audio_file.read()
        audio_file.close()
    
    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=48000,
        language_code='ko-KR')

    # 오디오 파일 분석
    response = client.recognize(config=config, audio=audio)
    print("result:",response.results)
    
    # 응답 언어가 있는지 여부 판단
    if response.results == []:
        var = False
    else:
        for result in response.results:
            script = result.alternatives[0].transcript    
            print(script) 
        # 영화 추천 포함 여부 판단
        var = "영화 추천" in script
    
    return var


def audio_preprocessing(filename: str) -> list:
    """오디오 전처리"""
    file_full: str = UPLOAD_DIRECTORY + filename
    audioSegment = AudioSegment.from_file(file_full)
    audioSegment = audioSegment.set_sample_width(sample_width=2)
    new_file_path = file_full.replace('webm', 'wav')
    audioSegment.export(new_file_path, format='wav', bitrate = '16k')
    print(audioSegment.sample_width)
    xf, _ = librosa.load(file_full)
    mfcc_1 = librosa.feature.mfcc(y=xf, sr=16000, n_mfcc=5, n_fft=400, hop_length=160)
    mfcc_1 = scale(mfcc_1, axis=1)
    feature = np.mean(mfcc_1.T, axis=0) 
    
    return [feature,new_file_path]

def cossim_matrix(a, b):
    """코사인 유사도 구하기"""
    cossim_values = cosine_similarity(a.values, b.values)
    cossim_df = pd.DataFrame(data=cossim_values, columns = a.index.values, index=a.index)
    return cossim_df


def item_sparse_matrix(ratings_df):
    """아이템 기반 협업 필터링"""
    sparse_matrix = ratings_df.groupby('movieId').apply(lambda x: pd.Series(x['rating'].values, index=x['userId'])).unstack()
    sparse_matrix.index.name = 'movieId'

    item_sparse_matrix = sparse_matrix.fillna(0)
    item_cossim_df = cossim_matrix(item_sparse_matrix, item_sparse_matrix)

    userId_grouped = ratings_df.groupby('userId')
    item_prediction_result_df = pd.DataFrame(index=list(userId_grouped.indices.keys()), columns=item_sparse_matrix.index)

    for userId, group in userId_grouped:
        # user가 rating한 movieId * 전체 movieId
        user_sim = item_cossim_df.loc[group['movieId']]
        # user가 rating한 movieId * 1
        user_rating = group['rating']
        # 전체 movieId * 1
        sim_sum = user_sim.sum(axis=0)
        # userId의 전체 rating predictions (8938 * 1)
        pred_ratings = np.matmul(user_sim.T.to_numpy(), user_rating) / (sim_sum+1)
        item_prediction_result_df.loc[userId] = pred_ratings
        
    return item_prediction_result_df

def movie_recommend_top_10(emotion, userId) -> dict:
    """영화 추천 top 10 추출"""
    global movie_df
    movie_df = movie_df_copy.copy()
    seen_movie = list(ratings_df[ratings_df["userId"] == userId]["movieId"].unique())
    movie_df.set_index("movieId", inplace=True)
    movie_df.drop(seen_movie, inplace=True)
    movie_df.reset_index(inplace=True)
    if emotion == 'anger':
        '''
        포함 : 코미디
        미포함 : 스릴러
        '''
        sample_df = movie_df[movie_df["genres"].str.contains("Comedy") & (~movie_df["genres"].str.contains("Thriller"))
                            & (~movie_df["genres"].str.contains("Horror")) & (~movie_df["genres"].str.contains("Crime"))
                            & (~movie_df["genres"].str.contains("Mystery")) & (~movie_df["genres"].str.contains("War"))]
    elif emotion == 'sad':
        '''
        포함 : 코미디, 액션 (참고. 범죄영화도 우울을 해소시키는 경향이 나타났지만 포함시키지 않은게 좋다고 판단하여 뺌)
        미포함 : 판타지, 드라마
        '''
        sample_df = movie_df[movie_df["genres"].str.contains("Comedy") & (movie_df["genres"].str.contains("Action"))
                          & (~movie_df["genres"].str.contains("Fantasy")) & (~movie_df["genres"].str.contains("Drama"))]
    else:
        sample_df = movie_df.copy()
    
    item_pred = item_sparse_matrix(ratings_df)
    
    item = item_pred.loc[userId].reset_index()
    item.columns = ["movieId","pred_rate"]
    item["movieId"] = item["movieId"].astype('int64')
    
    sample_df = sample_df.reset_index()
    result = pd.merge(sample_df, item, on="movieId")
    
    top10_movie = result.sort_values(by="pred_rate", ascending=False)[:10].reset_index(drop=True)
       
    return top10_movie.to_dict('index')


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

    return new_file_path


def audio_predict(x) -> int:
    """결과값 예측"""
    result = MODEL.predict(x)
    
    return result[0].tolist()

# ----------------------------------------------------------------------------------------------------------------------------------


UPLOAD_DIRECTORY = './tmp/'
TEMP_DIRECTORY = './temp/'

if not os.path.exists(UPLOAD_DIRECTORY):
    os.mkdir(UPLOAD_DIRECTORY)

app = Flask(__name__)
CORS(app=app, resources={r'*': {'origins': '*'}})

# NOTE How about using `fs` save on ram and then convert?
@app.route('/receive', methods=['POST'])
def form() -> Response:
    # 여기는 나중에 userid 세션으로 받아야함
    userId = 2
    
    """Get wav file"""
    file = request.files['file']

    if file.filename is not None:
        filename = secure_filename(filename=file.filename)
        file.save(os.path.join(UPLOAD_DIRECTORY, filename))
        # 영화추천을 포함해서 제대로 말했다면
        _x_val, new_file_path = audio_preprocessing(file.filename)
        print("new_file_path", new_file_path)
        print("file.filename", file.filename)
        if stt(new_file_path):
            predict_result = audio_predict([_x_val])
            top10 = movie_recommend_top_10(Label[predict_result],userId)
            return jsonify({'status': 'success', 'result': Label[predict_result], 'top10' : top10})
        else:
            return jsonify({'status': 'fail'})
    else:
        return jsonify({'status': 'fail'})


# NOTE This page is not need
@app.route('/', methods=['GET'])
def hello() -> str:
    """Render html"""
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
