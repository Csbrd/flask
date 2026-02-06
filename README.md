# 클라우드 서버 api 활용 자동화
NHN Cloud 환경에서 **VPC, Subnet, Security Group, Key Pair, Instance**를 한 번의 실행으로 자동으로 구축하는 스크립트

## 구성 환경
- **Language**: Python3.8+
- **OS**: Ubuntu 24.04 LTS
- **Instance Type**: m2.c1m2

## 파일 구조
- 'nhncloud_main.py': 전체 프로세스 제어 및 사용자 입력 처리
- 'nhncloud_util.py': NHN Cloud API 호출 및 리소스 생성 로직
- 'nhncloud_config.py': API 엔드포인트 및 사용자 인증 정보

## 사용하게된다면
<img width="1024" height="1024" alt="Gemini_Generated_Image_8o47dn8o47dn8o47" src="https://github.com/user-attachments/assets/f886a80f-90c5-4fc6-bfec-0bf309e18977" />


## 시작하기

### 모듈 다운로드
pip install requests


### nhncloud_config.py 파일 수정
먼저 config파일에 들어가 **TENANT_ID**, **USERNAME**, **PASSWORD**이 세 가지 설정값만 본인의 것으로 바꿔주면 된다.

.env 파일이 없다면 생성 후 개인 정보 기입을 하는 것을 권장한다.

### 실행하기
nhncloud_main.py 파일 실행
