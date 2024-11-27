import pyotp
import qrcode
from io import BytesIO

def generate_totp_secret():
    return pyotp.random_base32()

def generate_qr_code(secret, username):
    totp = pyotp.TOTP(secret)
    uri = totp.provisioning_uri(name=username, issuer_name="Login System")
    qr = qrcode.QRCode(box_size=5, border=1)
    qr.add_data(uri)
    qr.make(fit=True)
    # Create an image in memory
    img = qr.make_image(fill_color="black", back_color="white")
    # Save the image to a byte stream
    img_byte_arr = BytesIO()
    img.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr

def validate_totp(secret, totp_token):
    totp = pyotp.TOTP(secret)
    return totp.verify(totp_token)

