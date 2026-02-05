import requests

tenantID = "d847fb3ea6ae4de9aa99e78c5d19bfa3"
tokenID = "gAAAAABpgttH8YjQKUHXDpAXzooEXPRXxnu3qPMwf-PRxolO0odzgZdRJgLcNJ6HPpnbHiFhrcy1NdQ221ZdwLBj6culUHH9pxHINXCy2tJMv16oftqAaknRK6U4Qect3suVXdKl8Advgc03pYT1LI6jwCQMFBN9szGVIua3qzIaCSl3RzFf83E"
url_instance = "https://kr1-api-instance-infrastructure.nhncloudservice.com"
uri_instance = f"/v2/{tenantID}/servers"
instance_name = "api-instance"
instance_cidr = "10.0.0.0/8"
ubuntu_id = '7342b6e2-74d6-4d2c-a65c-90242d1ee218'
instancetype_id = 'a4b6a0f7-aeff-4d78-a8d5-7de9f007012d'

header  = {
    'X-Auth-Token': tokenID
}

body = {
    "server": {
    "name": instance_name,
    "flavorRef": instancetype_id,
    "networks": [{
        "uuid": "564ba216-c15c-46c4-bf61-3c3c571c64ae"
    }],
    "availability_zone": "kr-pub-a",
    "key_name": "cs-key",
    "max_count": 1,
    "min_count": 1,
    "block_device_mapping_v2": [{
        "source_type": "image",
        "uuid": ubuntu_id,
        "boot_index": 0,
        "volume_size": 40,
        "destination_type": "volume",
        "delete_on_termination": 1
    }],
    "security_groups": [{
        "name": "default"
    }]
    }
}

response_instance = requests.post(url_instance + uri_instance, headers=header, json=body)
if response_instance.status_code == 202: # 인스턴스 생성 성공은 보통 202입니다.
    print("인스턴스 생성 요청 성공")
else:
    print(f"생성 실패: {response_instance.status_code}")
    print(f"상세 에러 내용: {response_instance.text}") # 이 부분을 꼭 확인하세요!