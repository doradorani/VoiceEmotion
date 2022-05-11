# ![그룹 378](https://user-images.githubusercontent.com/96163167/167744810-3f1897f6-36a4-41eb-8877-9e409d9d1389.png)Nemotion 감정 기반 영화 추천 서비스 보이스 챗봇
> KT AIVLE SCHOOL 1기 AI 15조 - 부산 경남 1반 3조
> 
> __당신의 감정__ , __Nemotion__ = __Ne__ + __Emotion__
>
> ![썸네일](https://user-images.githubusercontent.com/96163167/167752978-c92ad4ef-b6c7-4408-8e76-253daaae9ef7.jpg)
>
> ## 개발자
> __권윤경 김란희 임성현__
>
> ## 프로젝트 기간
> 2022.04.11 ~ 2022.05.11
> 
> ## 담당 코치님
> 정호용 코치님
<br/>
<br/>

- [실행](#1-실행)
- [개요](#2-개요)
  - [주제](#주제)
  - [선정배경 및 기대효과](#선정배경-및-기대효과)
  - [주요기술](#주요기술)
  - [UI](#UI)
  - [프로젝트 폴더 설명](#프로젝트-폴더-설명)
- [아키텍처](#3-아키텍처)
  - [ERD설계](#erd설계)
  - [아키텍처 정의서](#아키텍처-정의서)
  - [ServiceFlow](#service-flow)
- [환경 및 버전](#4-환경-및-버전)
  - [Environment](#environment)
  - [Django](#django)
  - [Flask](#flask)
  - [Modeling](#modeling)
- [팀원 역할](#5.팀원-역할)
- [시연 영상](#6.시연-영상)
- [PPT](#7-ppt)
<br/>
<br/>

# 1. 실행
---

- requirements.txt 적용법

```bash
pip install -r requirements.txt
```
<br/>

- [Backend](backend/) 실행하기

  Root directory 에서 실행됨

  1. using make `make -B backend`
  2. using *sh (bash, zsh, ash, sh) `cd backend && python app.py`
  3. Powershell `cd backend; python app.py`

<br/>

- django 실행하기

```bash
python manage.py makemigrations
python manage.py migrate
python manage.py inspectdb
python manage.py runserver
```
<br/>

- google.cloud.speech API 사용

  conda 가상환경 실행 후 설치
  ```bash
  conda install -c conda-forge google-cloud-speech
  ```

<br/>
<br/>

# 2. 개요
---
## 주제
- 오늘 무슨 영화를 보고 싶은지 결정을 못하셨다면 니모션에게 __'영화 추천해줘'__ 한 마디만 말해보세요.
- 사용자의 음성이 성공적으로 입력되면 __감정을 분석__ 합니다.
- 감정 분석 결과를 바탕으로 다양한 장르의 __영화를 사용자에게 추천__ 합니다.
- 기존의 영화 추천시스템과 달리 실시간으로 변화하는 감정을 이용하여 주관적인 사용자 취향을 즉각적으로 반영하여 만족도를 상승시켜 줍니다.
<br/>
<br/>

## 선정배경 및 기대효과
- 전 세계 감정 분석 시장은 2018년 20억 9020만 달러에서 __연평균 성장률 17.05%로 증가__ 하여, 2023년에는 45억 9330만 달러에 이를 것으로 전망
- 그 중 음성 분석은 2019년 4억 9700만 달러에서 __연평균 성장률 14.9%로 증가__ 하여, 2024년에는 9억 9300만 달러에 이를 것으로 전망

![시장 규모](https://user-images.githubusercontent.com/96163167/167738929-4742fbc3-0321-4df9-9d9f-2d038dd4e08e.jpg)

- 넷플릭스, 왓차와 같은 플랫폼에서는 현재 인기가 많은 영화나 사용자가 봤던 영화를 기반으로 추천을 해주는 서비스를 제공
- 감정기반 서비스를 확대하여 음악, 도서, 광고, 쇼핑, 여행, 음악과 같은 다양한 컨텐츠에 추천 시스템을 적용가능
<br/>
<br/>

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
<br/>
<br/>

## UI/UX
UI/UX 설계 도안 : https://xd.adobe.com/view/8957327b-6282-4145-bad6-ceb04a5654f1-dc04/?fullscreen
![메인화면](https://user-images.githubusercontent.com/96163167/167738410-f34e647d-6204-4872-ac94-06f42f450066.png)


## 프로젝트 폴더 설명
- `backend` : Flask API에서 음원을 받아 감정분석, 영화 추천 시스템을 돌리는 폴더
- `board` : 서비스의 문의사항, 회원 정보 수정에 관한 기능 폴더
- `member` : 서비스의 회원가입, 로그인, 로그아웃에 관한 기능 폴더
- `model` : 서비스의 AI 모델 코드 폴더
- `service` : Flask API에서 데이터를 전송받아 사용자에게 보이스 챗봇 형식으로 보여주는 기능 폴더
<br/>
<br/>

# 3. 아키텍처
---
## ERD설계
링크 : https://www.erdcloud.com/d/XXKkK8m77SjPrCCTJ
![ERD](https://user-images.githubusercontent.com/96163167/167752934-2b7e9afc-e9be-48d5-9964-a32381997b4f.png)
<br/>
<br/>

## 아키텍처 정의서
![아키텍처 정의서](https://user-images.githubusercontent.com/96163167/167755062-a8dbf217-75b5-4c8f-a4c8-8aa8f2040a9a.png)
<br/>
<br/>

## Service Flow
![서비스 플로우](https://user-images.githubusercontent.com/96163167/167745556-445d2220-2084-426c-8ce5-0e02f9e8103c.jpg)
<br/>
<br/>


# 4. 환경 및 버전
---


## Environment

- Linux ( Docker )

### Django

- Python 3.8

### Flask API

- Flask 2.1.1

### Modeling

- Python 3.6
- tensorflow 2.8.0
- keras 2.8.0
- librosa 0.91
- xgboost 0.90
- scikit-learn 1.0.2

<br/>
<br/>

# 5. 팀원 역할
---
![프로젝트 소개](https://user-images.githubusercontent.com/96163167/167740554-dba9db93-a288-4eec-ac20-837baba7ac5e.png)

| 이름                                        | 담당 직무                              |
| ------------------------------------------- | --------------------------------------|
| [권윤경](https://github.com/yoonkyeongkwon) | ML / AI Modeling                       |
| [김란희](https://github.com/doradorani)     | Frontend / UI/UX Design                |         
| [배성훈](https://github.com/fish895623)     | Additional Manpower                    |
| [임성현](https://github.com/dlatjdgus95)    | Backend, Server Management             |
<br/>
<br/>

# 6. 시연 영상
---
시연 영상 : https://youtu.be/MDiKSU7RE-Q
<br/>
<br/>

# 7. PPT
---
발표 PPT : https://drive.google.com/file/d/1JhGx2dA_lZFiZ6aVgLMYC3KVj3_JPQn8/view?usp=sharing
