import os
import requests

# --- URL ---
domain = "https://invitations.uz"

# --- OS PATH ---
# path = "D:\MyFiles\domains\app\src"
path_os_all = os.path.abspath(__file__).split("/")
path_os = ""
for tmp in path_os_all:
    if tmp == "qr_bot":
        path_os += f"{tmp}"
        break
    path_os += f"{tmp}/"


def contact_api(phone):
    path = "qr_by_phone"
    contact_req = requests.get(url=f"{domain}/api/{path}/{phone}/")
    contact = contact_req.json()
    if contact_req.status_code == 200:
        result = {
            'image': contact['message']['media'][:-1],
            'path': path_os,
            'status': contact_req.status_code
        }

        img_url = requests.get(url=f"{domain}{result['image']}")
        with open(f"{result['path']}{result['image']}", "wb") as file:
            file.write(img_url.content)
    else:
        result = {
            'status': contact_req.status_code
        }

    return result
