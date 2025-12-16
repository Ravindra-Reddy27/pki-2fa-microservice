import base64
import pyotp
import time


def generate_totp_code(hex_seed: str):
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode()

    totp = pyotp.TOTP(base32_seed)
    code = totp.now()

    # remaining seconds (0–29)
    valid_for = totp.interval - (int(time.time()) % totp.interval)

    return code, valid_for


def verify_totp_code(hex_seed: str, code: str, valid_window: int = 1) -> bool:
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode()

    totp = pyotp.TOTP(base32_seed)
    return totp.verify(code, valid_window=valid_window)
