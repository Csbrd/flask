import requests

tenantID = "d847fb3ea6ae4de9aa99e78c5d19bfa3"
url_keypair = "https://kr1-api-instance-infrastructure.nhncloudservice.com"
uri_keypair = f"/v2/{tenantID}/os-keypairs"
url = "https://api-identity-infrastructure.nhncloudservice.com"
uri = "/v2.0/tokens"

body = {
"auth": {
    "tenantId": tenantID,
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




for i in range(1, 6):
    key_name = f"my-keypair-{i}"
    uri_del = f"/v2/{tenantID}/os-keypairs/{key_name}"
    body_ = {
    "keypair": {
        "name": key_name
    }
}
    respons_del = requests.delete(url_keypair + uri_del, headers=header)
#     response_keypair = requests.post(url_keypair + uri_keypair, headers=header, json=body_)

# if response_keypair.status_code == 200:
#     print("생성 성공")
# else:
#     print(f"생성 실패, {response_keypair.status_code}")

if respons_del.status_code in [202, 204]:
    print(f"성공 {key_name} 삭제 요청 완료")
elif respons_del.status_code == 404:
    print(f"{key_name}은(는) 이미 존재하지 않습니다")
else:
    print(f"실패: {key_name} - 상태 코드: {respons_del.status_code}")
    print(f"실패 사유: {respons_del.text}")