import requests


tenantID = "d847fb3ea6ae4de9aa99e78c5d19bfa3"
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

response = requests.get(url + uri, json=body)
print(response)