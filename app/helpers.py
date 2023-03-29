import qrcode
import settings


def generate_qr_code(string):
    url = f"{settings.domain}/api/ticket/deactivate/{string}/"
    qr = qrcode.make(url)
    path = f"media/{string}.png"
    qr.save(path)
    img = open(path, "rb")
    return img
