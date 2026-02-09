# flask를 이용한 점심 메뉴 추천 웹 사이트
제미나이 AI와 카카오맵 API를 활용하여 점심 메뉴를 추천해주고, 본인이 먹고 싶은 메뉴의 위치를 알 수 있다.
## 주요 기능
- **랜덤 메뉴 추천**: 한식, 일식, 중식 등 카테고리별 랜덤 메뉴 추출
- **AI 메뉴 제안**: Google Gemini API를 활용한 스마트한 메뉴 추천 (업그레이드 예정)
- **실시간 맛집 검색**: 추천된 메뉴를 카카오맵 키워드 검색과 연동하여 주변 맛집 정보 제공
- **슬랙 연동**: 슬랙 커맨드(`/점심`)를 통해 채널 내에서 즉시 메뉴 추천 가능
## 구성 환경
- **Backend**: Python 3.14+, Flask
- **Deployment**: Render
- **API**: Kakao Map API, Google Generative AI (Gemini), Slack API
- **WSGI**: Gunicorn
## 시작하기
### 저장소 복제
`git clone https://github.com/Csbrd/flask`
### 라이브러리 설치
`pip install -r requirements.txt`
### 실행하기
`python app.py`(=`py app.py`)
