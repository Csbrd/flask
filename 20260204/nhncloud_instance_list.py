import requests

tenantID = "d847fb3ea6ae4de9aa99e78c5d19bfa3"
tokenID = "gAAAAABpgttH8YjQKUHXDpAXzooEXPRXxnu3qPMwf-PRxolO0odzgZdRJgLcNJ6HPpnbHiFhrcy1NdQ221ZdwLBj6culUHH9pxHINXCy2tJMv16oftqAaknRK6U4Qect3suVXdKl8Advgc03pYT1LI6jwCQMFBN9szGVIua3qzIaCSl3RzFf83E"
url_instance = "https://kr1-api-instance-infrastructure.nhncloudservice.com"
uri_instance = f"/v2/{tenantID}/servers"

header  = {
    'X-Auth-Token': tokenID
}

response_instance = requests.get(url_instance + uri_instance, headers=header)
print(response_instance.json())