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
key_name = "cs-key-123"
body_ = {
    "keypair": {
        "name": key_name
    }
}


def request(baseurl, uri, METHOD, token, header=None, body_=None):
    url =f"{baseurl}{uri}"
    header = {
        "X-Auth-Token": token
    }
    return requests.Request(METHOD, url, headers=header, json=body_)

resault = request()
print(resault)