def run_quickstart():
    import io
    import os
    from pathlib import Path

    os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="C:/Users/User/Downloads/aivlebigproject-348610-27ad2f7a9168.json"

    # Google Cloud client 라이브러리
    from google.cloud import speech

    # 클라이언트 인스턴스화
    client = speech.SpeechClient()

    BASE_DIR = Path(__file__).resolve().parent.parent
    
    # 오디오 파일 이름
    file_name = os.path.join(BASE_DIR,'backend/tmp/1651466227802.wav')
    print(file_name)
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
    print("result:",type(response.results))
    
    for result in response.results:
        script = result.alternatives[0].transcript
        
    var = "영화 추천" in script
    if var:
        print("ok")
    else:
        print("다시 한번 말씀해주세요")

if __name__ == '__main__':
    run_quickstart()
