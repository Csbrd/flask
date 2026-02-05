import requests
import json

# 1. 설정 정보
PROJECT_ID = 'd847fb3ea6ae4de9aa99e78c5d19bfa3' # 보내주신 데이터에서 추출한 ID
REGION_ENDPOINT = 'https://kr1-api-instance-infrastructure.nhncloudservice.com'

# 2. Flavor 상세 목록 조회 URL (상세 정보를 위해 /detail 사용)
url = f"{REGION_ENDPOINT}/v2/{PROJECT_ID}/flavors/detail"

url = "https://api-identity-infrastructure.nhncloudservice.com"
uri = "/v2.0/tokens"

body = {
"auth": {
    "tenantId": PROJECT_ID,
    "passwordCredentials": {
        "username": "test03",
        "password": "ckdtjs123!@#"
    }
}
}

response = requests.post(url + uri, json=body)

tokenID = response.json()['access']['token']['id']

header  = {
    'X-Auth-Token': tokenID
}

# 3. API 호출
response = requests.get(url, headers=header)

if response.status_code == 200:
    flavors = response.json().get('flavors', [])
    
    # 우리가 찾는 m2.c1m2 찾기
    target_name = "m2.c1m2"
    flavor_id = None
    
    print(f"--- '{target_name}' 탐색 결과 ---")
    for f in flavors:
        if f['name'] == target_name:
            flavor_id = f['id']
            print(f"이름: {f['name']}")
            print(f"ID (flavorRef): {f['id']}")
            print(f"vCPUs: {f['vcpus']}, RAM: {f['ram']}MB")
            break
            
    if not flavor_id:
        print(f"'{target_name}'을 찾을 수 없습니다. 목록을 다시 확인해 보세요.")
else:
    print(f"조회 실패: {response.status_code}")
    print(response.text)