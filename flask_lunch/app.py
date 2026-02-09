import random
from flask import Flask, render_template, request, jsonify
import os

app = Flask(__name__)

# 메뉴 데이터 구성
FOOD_DATA = {
    "KOREAN": ["제육볶음", "김치찌개", "비빔밥", "순대국", "불고기", "떡볶이", "닭갈비", "육회비빔밥"],
    "JAPANESE": ["초밥", "돈카츠", "텐동", "라멘", "사케동", "우동", "가츠동", "소바"],
    "CHINESE": ["짜장면", "짬뽕", "마라탕", "꿔바로우", "볶음밥", "딤섬", "양꼬치"],
    "WESTERN": ["파스타", "수제버거", "스테이크", "피자", "샌드위치", "리조또"],
    "LIGHT": ["샐러드", "포케", "샌드위치", "그릭요거트", "월남쌈"]
}

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/spin', methods=['POST'])
def spin():
    # 사용자가 직접 입력한 메뉴 확인
    user_menu = request.form.get('user_menu', '').strip()
    category = request.form.get('category', 'ALL')
    
    if user_menu:
        # 1순위: 사용자가 직접 입력한 메뉴 사용
        picked = user_menu
        mode = "직접 선택"
    else:
        # 2순위: 카테고리 랜덤 추출
        if category == "ALL":
            all_menus = sum(FOOD_DATA.values(), [])
            picked = random.choice(all_menus)
        else:
            picked = random.choice(FOOD_DATA.get(category, FOOD_DATA["KOREAN"]))
        mode = "랜덤 추천"
    
    # 카카오맵 검색 링크 생성
    search_url = f"https://map.kakao.com/link/search/{picked}"
    
    return render_template('index.html', result=picked, url=search_url, mode=mode)

@app.route('/slack/spin', methods=['POST'])
def slack_spin():
    # 슬랙은 사용자가 입력한 추가 텍스트를 'text'라는 키로 보냅니다.
    # 예: '/점심 제육볶음' 이라고 치면 user_text는 '제육볶음'이 됩니다.
    user_text = request.form.get('text', '').strip()
    
    if user_text:
        picked = user_text
    else:
        # 모든 메뉴에서 랜덤 추출
        all_menus = sum(FOOD_DATA.values(), [])
        picked = random.choice(all_menus)
    
    search_url = f"https://map.kakao.com/link/search/{picked}"
    
    # 슬랙 형식에 맞는 JSON 응답
    response = {
        "response_type": "in_channel", # 채널의 모든 사람이 결과를 볼 수 있게 함
        "text": f"🍱 오늘의 점심 추천: *{picked}* 어때요?",
        "attachments": [
            {
                "text": f"<{search_url}|📍 근처 맛집 지도 보기>",
                "color": "#4f46e5"
            }
        ]
    }
    
    return jsonify(response)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    
    # host="0.0.0.0"은 외부 접속을 허용하는 핵심 설정입니다.
    app.run(host="0.0.0.0", port=port)