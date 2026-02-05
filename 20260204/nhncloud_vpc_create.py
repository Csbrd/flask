import requests

tenantID = "d847fb3ea6ae4de9aa99e78c5d19bfa3"
tokenID = "gAAAAABpgttH8YjQKUHXDpAXzooEXPRXxnu3qPMwf-PRxolO0odzgZdRJgLcNJ6HPpnbHiFhrcy1NdQ221ZdwLBj6culUHH9pxHINXCy2tJMv16oftqAaknRK6U4Qect3suVXdKl8Advgc03pYT1LI6jwCQMFBN9szGVIua3qzIaCSl3RzFf83E"
url_vpc = "https://kr1-api-network-infrastructure.nhncloudservice.com"
uri_vpc = "/v2.0/vpcs"
vpc_name = 'api-vpc'
vpc_cidr = '10.0.0.0/16'

header  = {
    'X-Auth-Token': tokenID
}

data = {
    "vpc": {
        "name": vpc_name,
        "cidrv4": vpc_cidr
    }
}

response_vpc = requests.post(url_vpc + uri_vpc, headers=header, json=data)
if response_vpc.status_code == 201:
    print("VPC 생성 성공")
else:
    print(f"생성 실패: {response_vpc.status_code}")