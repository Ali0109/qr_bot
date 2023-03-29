import os
import requests
import settings

domain = settings.domain


def contact_api(phone):
    path = "qr_by_phone"
    contact_req = requests.get(url=f"{domain}/api/{path}/{phone}/")
    result = contact_req

    return result
