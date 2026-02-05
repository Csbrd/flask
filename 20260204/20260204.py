import requests

url = "https://api-identity-infrastructure.nhncloudservice.com"
url = "https://jsonplaceholder.typicode.com/posts"
data = {
    "title": "공부 중",
    "body": "파이썬 열심히 공부 중",
    "userId": 10
}

response = requests.post(url,json=data)
print("응답 코드:", response.status_code)
print("응답 본문:", response.text)