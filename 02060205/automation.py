import requests
import json
import sys
import ipaddress
from dotenv import load_dotenv
import os

# --- [1. 설정 정보] ---
AUTH_URL = "https://api-identity-infrastructure.nhncloudservice.com/v2.0/tokens"
TENANT_ID = os.getenv("nhn_cloud_tenantID")
USERNAME = os.getenv("nhn_cloud_id")
PASSWORD = os.getenv("nhn_cloud_pw")

# 리전 엔드포인트 및 이미지 UUID 설정 (예: 판교 KR1 리전 기준)
NW_URL = "https://kr1-api-network-infrastructure.nhncloudservice.com/v2.0"
COMPUTE_URL = f"https://kr1-api-instance-infrastructure.nhncloudservice.com/v2/{TENANT_ID}"

# 🌟 Ubuntu 24.04 이미지 UUID (콘솔에서 확인된 값을 여기에 넣으세요)
# 리전마다 다르므로, 실제 환경의 UUID로 한 번만 교체해 주시면 클라이언트는 입력할 필요가 없습니다.
UBUNTU_24_UUID = "7342b6e2-74d6-4d2c-a65c-90242d1ee218"
M2_C1M2_UUID = "a4b6a0f7-aeff-4d78-a8d5-7de9f007012d"

# --- [2. 유효성 검증 함수] ---
def create_keypair(headers, key_name):
    """키 페어를 생성하고 개인키(.pem) 파일을 로컬에 저장"""
    print(f"\nStep 1: 키 페어 '{key_name}' 생성 중...")
    url = f"{COMPUTE_URL}/os-keypairs"
    res = requests.post(url, headers=headers, json={"keypair": {"name": key_name}})
    
    if res.status_code == 200:
        private_key = res.json()['keypair']['private_key']
        filename = f"{key_name}.pem"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(private_key)
        print(f"✅ 키 저장 완료: {filename}")
    elif res.status_code == 409:
        print(f"ℹ️ '{key_name}'은 이미 존재합니다. 기존 키를 사용하여 인스턴스를 생성합니다.")
    else:
        print(f"❌ 키 생성 실패: {res.text}"); sys.exit()


def validate_vpc_cidr():
    allowed = [ipaddress.ip_network("10.0.0.0/16"), ipaddress.ip_network("172.16.0.0/16"), ipaddress.ip_network("192.168.0.0/16")]
    while True:
        val = input(f"\n[VPC] 생성할 대역 입력 (10.0.0.0/16, 172.16.0.0/16, 192.168.0.0/16): ")
        try:
            if ipaddress.ip_network(val) in allowed: return val
            print("❌ 허용되지 않은 대역입니다.")
        except ValueError: print("❌ CIDR 형식이 아닙니다.")

def validate_subnet_cidr(vpc_cidr_str):
    vpc_net = ipaddress.ip_network(vpc_cidr_str)
    while True:
        val = input(f"[Subnet] 생성할 대역 입력 ({vpc_cidr_str} 범위 내): ")
        try:
            if ipaddress.ip_network(val).subnet_of(vpc_net): return val
            print(f"❌ VPC 대역({vpc_cidr_str})을 벗어났습니다.")
        except ValueError: print("❌ CIDR 형식이 아닙니다.")

# --- [3. 실행 함수] ---

def get_auth_token():
    payload = {"auth": {"tenantId": TENANT_ID, "passwordCredentials": {"username": USERNAME, "password": PASSWORD}}}
    res = requests.post(AUTH_URL, json=payload)
    if res.status_code == 200: return res.json()['access']['token']['id']
    else:
        print("❌ 인증 실패! 설정을 확인하세요."); sys.exit()

def run_automation():
    print("🚀 NHN Cloud 인프라 생성 스크립트 (Ubuntu 24.04 전용)")
    
    # 입력 받기
    key_name = input("새로 만들 키 페어 이름: ")
    vpc_name = input("VPC 이름: ")
    vpc_cidr = validate_vpc_cidr()
    sub_name = input("서브넷 이름: ")
    sub_cidr = validate_subnet_cidr(vpc_cidr)
    sg_name = input("보안 그룹 이름: ")
    allow_ip = input("SSH(22) 허용할 특정 IP/대역 (예: 211.x.x.x/32): ")
    inst_name = input("인스턴스 이름: ")

    token = get_auth_token()
    headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}

    try:
        # 1. 키 페어 생성 및 파일 저장
        create_keypair(headers, key_name)
        # 2. VPC 생성
        print("\nStep 2: VPC 생성 중...")
        vpc_payload = {
            "vpc": {
                "name": vpc_name,
                "cidrv4": str(vpc_cidr)
            }
        }
        
        response = requests.post(f"{NW_URL}/vpcs", headers=headers, json=vpc_payload)

        if response.status_code == 201:
            v_res = response.json()
            vpc_id = v_res['vpc']['id']
            print(f"✅ VPC 생성 성공! ID: {vpc_id}")
        else:
            print(f"❌ VPC 생성 실패 (상태 코드: {response.status_code})")
            print(f"❌ 에러 원인: {response.text}")
            sys.exit()

        # 3. 서브넷 생성
        print("Step 3: 서브넷 생성 중...")
        
        sub_payload = {
            "vpcsubnet": {
                "name": sub_name, 
                "vpc_id": vpc_id,      # 🌟 이건 아까 에러가 안 났으니 유지!
                "cidr": sub_cidr       # 🌟 'cidrv4'가 아니라고 하니 다시 'cidr'로 변경!
            }
        }
        
        sub_res = requests.post(f"{NW_URL}/vpcsubnets", headers=headers, json=sub_payload)

        if sub_res.status_code == 201:
            sub_data = sub_res.json()
            # 응답 데이터 구조에 맞춰 ID 추출
            subnet_id = sub_data['vpcsubnet']['id']
            print(f"✅ 서브넷 생성 성공! (ID: {subnet_id})")
        else:
            print(f"❌ 서브넷 생성 실패 (상태 코드: {sub_res.status_code})")
            print(f"❌ 에러 내용: {sub_res.text}")
            sys.exit()

        # 4. 보안 그룹 설정
        print("Step 4: 보안 그룹 설정 중...")
        sg_res = requests.post(f"{NW_URL}/security-groups", headers=headers, json={"security_group": {"name": sg_name}}).json()
        sg_id = sg_res['security_group']['id']
        requests.post(f"{NW_URL}/security-group-rules", headers=headers, json={
            "security_group_rule": {"security_group_id": sg_id, "direction": "ingress", "protocol": "tcp", "port_range_min": 22, "port_range_max": 22, "remote_ip_prefix": allow_ip}
        })

        # 5. 인스턴스 생성 (Ubuntu 24.04 / m2.t1m2 고정)
        print(f"Step 5: 인스턴스 생성 중 (OS: Ubuntu 24.04, Flavor: m2.t1m2)...")
        server_payload = {
            "server": {
                "name": inst_name,
                "imageRef": UBUNTU_24_UUID,
                "flavorRef": M2_C1M2_UUID,
                "networks": [{"uuid": vpc_id}],
                "security_groups": [{"name": sg_name}],
                "block_device_mapping_v2": [{
                    "uuid": UBUNTU_24_UUID,      # 사용할 이미지의 ID
                    "source_type": "image",
                    "destination_type": "volume",
                    "boot_index": 0,
                    "volume_size": 30,           
                    "delete_on_termination": True # 인스턴스 삭제 시 디스크도 삭제
                }] 
            }
        }
        inst_res = requests.post(f"{COMPUTE_URL}/servers", headers=headers, json=server_payload)
        
        # 응답 상태 확인 (200 또는 202여야 성공)
        if inst_res.status_code in [200, 202]:
            print(f"\n✅ 인스턴스 생성 요청 성공!")
            print(f"📍 서버로부터 받은 응답: {inst_res.json()}")
        else:
            print(f"\n❌ 인스턴스 생성 실패 (상태 코드: {inst_res.status_code})")
            print(f"❌ 실패 상세 이유: {inst_res.text}") # 이 메시지가 정답입니다.
            sys.exit()
        print(f"\n✅ 인프라 생성 요청이 완료되었습니다!")

    except Exception as e:
        print(f"❌ 오류 발생: {e}")

if __name__ == "__main__":
    run_automation()