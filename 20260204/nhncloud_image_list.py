import requests

tenantID = "d847fb3ea6ae4de9aa99e78c5d19bfa3"
tokenID = "gAAAAABpgttH8YjQKUHXDpAXzooEXPRXxnu3qPMwf-PRxolO0odzgZdRJgLcNJ6HPpnbHiFhrcy1NdQ221ZdwLBj6culUHH9pxHINXCy2tJMv16oftqAaknRK6U4Qect3suVXdKl8Advgc03pYT1LI6jwCQMFBN9szGVIua3qzIaCSl3RzFf83E"
url_image = "https://kr1-api-image-infrastructure.nhncloudservice.com"
uri_image = "/v2/images"

header  = {
    'X-Auth-Token': tokenID
}

response_image = requests.get(url_image + uri_image, headers=header)
print(response_image.json())