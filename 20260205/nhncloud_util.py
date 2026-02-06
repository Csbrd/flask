import requests
import sys
from nhncloud_config import *

def get_non_empty_input(prompt):
    while True:
        val = input(prompt).strip()
        if val:
            return val
        print("⚠️  이 항목은 필수입니다. 값을 입력해주세요.")

def get_auth_token():
    payload = {"auth": {"tenantId": TENANT_ID, "passwordCredentials": {"username": USERNAME, "password": PASSWORD}}}
    res = requests.post(AUTH_URL, json=payload)
    if res.status_code == 200: return res.json()['access']['token']['id']
    else: print("❌ 인증 실패!"); sys.exit()

def create_keypair(headers, key_name):
    res = requests.post(f"{COMPUTE_URL}/os-keypairs", headers=headers, json={"keypair": {"name": key_name}})
    if res.status_code == 200:
        private_key = res.json()['keypair']['private_key']
        with open(f"{key_name}.pem", "w", encoding="utf-8") as f: f.write(private_key)
        return True
    return res.status_code == 409  # 이미 존재하면 True 취급

def create_vpc(headers, name, cidr):
    # 중복 체크
    vpcs = requests.get(f"{NW_URL}/vpcs", headers=headers).json().get('vpcs', [])
    if any(v['name'] == name for v in vpcs): return None, "VPC 이름 중복"
    
    res = requests.post(f"{NW_URL}/vpcs", headers=headers, json={"vpc": {"name": name, "cidrv4": str(cidr)}})
    return (res.json()['vpc']['id'], None) if res.status_code == 201 else (None, res.text)

def create_subnet(headers, name, vpc_id, cidr):
    res = requests.post(f"{NW_URL}/vpcsubnets", headers=headers, 
                        json={"vpcsubnet": {"name": name, "vpc_id": vpc_id, "cidr": cidr}})
    return (res.json()['vpcsubnet']['id'], None) if res.status_code == 201 else (None, res.text)

def create_security_group(headers, name, allow_ip="0.0.0.0/0"):
    sg_res = requests.post(f"{NW_URL}/security-groups", headers=headers, json={"security_group": {"name": name}}).json()
    sg_id = sg_res['security_group']['id']
    requests.post(f"{NW_URL}/security-group-rules", headers=headers, json={
        "security_group_rule": {"security_group_id": sg_id, "direction": "ingress", "protocol": "tcp", 
                                "port_range_min": 22, "port_range_max": 22, "remote_ip_prefix": allow_ip}
    })
    return sg_id

def create_instance(headers, name, vpc_id, sg_name, key_name):
    payload = {
        "server": {
            "name": name, "flavorRef": M2_C1M2_UUID, "key_name": key_name,
            "networks": [{"uuid": vpc_id}], "security_groups": [{"name": sg_name}],
            "block_device_mapping_v2": [{
                "uuid": UBUNTU_24_UUID, "source_type": "image", "destination_type": "volume",
                "boot_index": 0, "volume_size": 30, "delete_on_termination": True
            }]
        }
    }
    res = requests.post(f"{COMPUTE_URL}/servers", headers=headers, json=payload)
    return res.status_code in [200, 202], res.text