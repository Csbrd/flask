import requests

tenantID = "d847fb3ea6ae4de9aa99e78c5d19bfa3"
tokenID = "gAAAAABpgttH8YjQKUHXDpAXzooEXPRXxnu3qPMwf-PRxolO0odzgZdRJgLcNJ6HPpnbHiFhrcy1NdQ221ZdwLBj6culUHH9pxHINXCy2tJMv16oftqAaknRK6U4Qect3suVXdKl8Advgc03pYT1LI6jwCQMFBN9szGVIua3qzIaCSl3RzFf83E"
url_sn = "https://kr1-api-network-infrastructure.nhncloudservice.com"
uri_sn = "/v2.0/vpcsubnets"
subnet_name = 'api-subnet'
subnet_cidr = '10.0.10.0/24'

header  = {
    'X-Auth-Token': tokenID
}

data_sn = {
    "vpcsubnet": {
        "vpc_id": "564ba216-c15c-46c4-bf61-3c3c571c64ae",
        "cidr": subnet_cidr,
        "name": subnet_name
    }
}

response_subnet = requests.post(url_sn + uri_sn, headers=header, json=data_sn)
if response_subnet.status_code == 201:
    print("SUBNET 생성 성공")
else:
    print(f"생성 실패: {response_subnet.status_code}")