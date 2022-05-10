# Nemotion 감정 기반 영화 추천 서비스 보이스 챗봇
> KT AIVLE SCHOOL 1기 AI 15조 - 부산 경남 1반 3조
>
> ## 개발자
> 권윤경 김란희 임성현
>
> ## 프로젝트 기간
> 2022.04.11 ~ 2022.05.11

- [개요](#1-개요)
   -[주제](#주제)
   -[주요기술](#주요기술)
   -[UI](#UI)


# 1. 개요
---
## 주제
> 오늘 무슨 영화를 보고 싶은지 결정을 못하셨다면 니모션에게 '영화 추천해줘' 한 마디만 말해보세요.
> 사용자의 음성이 성공적으로 입력되면 감정을 분석합니다.
> 감정 분석 결과를 바탕으로 다양한 장르의 영화를 사용자에게 추천합니다.
> 기존의 영화 추천시스템과 달리 실시간으로 변화하는 감정을 이용하여 주관적인 사용자 취향을 즉각적으로 반영하여 만족도를 상승시켜 줍니다.


## 주요기술
STT
 - Google Speech API 사용

MFCC
 - 오디오 신호에서 추출할 수 있는 Feature
 1. 오디오 신호를 프레임 별로 나누어 FFT를 적용해 Spectrum 구하기
 2. Spectrum에 Mel Filter Bank를 적용해 Mel Spectrum 구하기
 3. Mel Spectrum Cepstral 분석을 적용해 MFCC 구하기


CNN
 - 인간의 시신경 구조를 모방한 기술
 1. 특징 추출: Convolution Layer와 Pooling Layer를 여러 겹 쌓는 형태
 2. 특징 추출과 클래스 분류 사이에 배열 형태로 만들어 주는 Flatten Layer 추가
 3. 클래스 분류 : Fully Connected Layer 추가


협업 기반 필터링
 - 많은 유저들로부터 모은 취향 정보들을 기반으로 하여 예측
 1. Item-based: 아이템과 아이템 간의 유사도를 기준
 2. User-based: 두 사용자 간의 유사도를 기준

## UI
> UI 초안 링크 : https://xd.adobe.com/view/8957327b-6282-4145-bad6-ceb04a5654f1-dc04/?fullscreen
![예시 이미지](https://raw.githubusercontent.com/ByungJun25/Wiki/master/Markdown/example_image.jpg)


- requirements.txt 적용법

```bash
pip install -r requirements.txt
```

- [Backend](backend/) 실행하기

  Root directory 에서 실행됨

  1. using make `make -B backend`
  2. using *sh (bash, zsh, ash, sh) `cd backend && python app.py`
  3. Powershell `cd backend; python app.py`

- django 실행하기 ( TODO )


---

MFCC를 이용하여 사용자의 기분을 파악한 후 현재 기분을 풀기 위해 알맞는 미디어 추천

## Environment

- Linux ( Docker )

### Django

- Python 3.8

### Modeling

- Python 3.6
- tensorflow
- librosa

## Contributors

| 이름                                        | 담당 직무                              |
| ------------------------------------------- | -------------------------------------- |
| [권윤경](https://github.com/yoonkyeongkwon) | ML / AI Modeling                       |
| [김란희](https://github.com/doradorani)     | Frontend / UI/UX Design 
|         
| [배성훈](https://github.com/fish895623)     | Additional Manpower
|
| [임성현](https://github.com/dlatjdgus95)    | Backend, Server Management
|
