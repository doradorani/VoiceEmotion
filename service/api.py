def run_quickstart():
    import io
    import os

    # Google Cloud client 라이브러리
    from google.cloud import speech


    # 클라이언트 인스턴스화
    client = speech.SpeechClient()


    # 오디오 파일 이름
    file_name = 'C:/aivlebigproject/VoiceEmotion/backend/tmp/1651198992313.wav'


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

    
    for result in response.results:
        print('Transcript: {}'.format(result.alternatives[0].transcript))

if __name__ == '__main__':
    run_quickstart()
