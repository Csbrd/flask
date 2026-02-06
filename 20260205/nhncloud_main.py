import sys
import ipaddress
import nhncloud_util as utils

def validate_vpc_cidr():
    # 사설 IP 대역 정의 (RFC 1918)
    # 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16
    while True:
        val = input(f"\n[VPC] 대역 입력 (예: 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16 등): ")
        try:
            user_net = ipaddress.ip_network(val)
            
            # 사설 IP 대역인지 검사
            if user_net.is_private:
                # NHN Cloud의 일반적인 권장사항: 너무 넓은 /8보다는 적당히 넓은 /12 ~ /16 추천
                if user_net.prefixlen > 24:
                    print("❌ VPC 대역이 너무 좁습니다. (24비트 이하 권장)")
                    continue
                return val
            else:
                print("❌ 사설 IP 대역(10.x, 172.16.x~31.x, 192.168.x)만 가능합니다.")
        except ValueError:
            print("❌ 올바른 CIDR 형식이 아닙니다. (예: 10.0.0.0/16)")

def valid_subnet_cidr(vpc_cidr):
    """
    VPC 대역을 기준으로 서브넷 대역의 유효성을 즉시 검사합니다.
    """
    vpc_net = ipaddress.ip_network(vpc_cidr)
    
    # 추천 서브넷 계산: VPC 대역 내의 첫 번째 /24 서브넷 생성
    # 만약 VPC가 /24보다 작다면(/25 등), VPC 전체를 기본값으로 설정
    try:
        recommended_sub = list(vpc_net.subnets(new_prefix=24))[0]
    except ValueError:
        recommended_sub = vpc_net

    while True:
        prompt = f"서브넷 대역 (추천: {recommended_sub}): "
        val = input(prompt).strip()
        
        # 엔터 입력 시 추천 대역 사용
        sub_input = val if val else str(recommended_sub)
        
        try:
            sub_net = ipaddress.ip_network(sub_input)
            
            # 핵심 로직: 서브넷이 VPC 대역의 하위 집합인지 확인
            if sub_net.subnet_of(vpc_net):
                return sub_input
            else:
                print(f"❌ 오류: 서브넷 {sub_input}은 VPC 대역 {vpc_cidr} 내에 포함되어야 합니다.")
                print(f"👉 다시 입력해주세요.")
        except ValueError:
            print("❌ 올바른 CIDR 형식이 아닙니다. (예: 10.0.1.0/24)")

def main():
    print("🚀 NHN Cloud 인프라 생성 자동화")
    
    # 1. 입력 수집
    key_name = utils.get_non_empty_input("키 페어 이름: ")
    vpc_name = utils.get_non_empty_input("VPC 이름: ")
    vpc_cidr = validate_vpc_cidr()
    sub_name = utils.get_non_empty_input("서브넷 이름: ")
    sub_cidr = valid_subnet_cidr(vpc_cidr)
    sg_name = utils.get_non_empty_input("보안 그룹 이름: ")
    allow_ip = input("SSH 허용 IP (예: 0.0.0.0/0): ")
    inst_name = utils.get_non_empty_input("인스턴스 이름: ")

    # 2. 인증 및 실행
    token = utils.get_auth_token()
    headers = {'X-Auth-Token': token, 'Content-Type': 'application/json'}

    # 3. 인프라 조립
    utils.create_keypair(headers, key_name)
    
    vpc_id, err = utils.create_vpc(headers, vpc_name, vpc_cidr)
    if err: print(f"❌ VPC 생성 실패: {err}"); sys.exit()
    
    sub_id, err = utils.create_subnet(headers, sub_name, vpc_id, sub_cidr)
    if err: print(f"❌ 서브넷 생성 실패: {err}"); sys.exit()
    
    utils.create_security_group(headers, sg_name, allow_ip)
    
    success, msg = utils.create_instance(headers, inst_name, vpc_id, sg_name, key_name)
    if success:
        print(f"\n✅ 모든 인프라 생성 성공! 인스턴스명: {inst_name}")
    else:
        print(f"❌ 인스턴스 생성 실패: {msg}")

if __name__ == "__main__":
    main()