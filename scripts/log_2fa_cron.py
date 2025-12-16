#!/usr/bin/env python3
"""
Cron script to log 2FA codes every minute
"""

import os
import sys
import base64
import datetime
import pyotp

SEED_PATH = "/data/seed.txt"


def main():
    # 1. Read seed safely
    if not os.path.exists(SEED_PATH):
        # Seed not available yet → exit silently
        return

    try:
        with open(SEED_PATH, "r") as f:
            hex_seed = f.read().strip()
    except Exception:
        return

    # Validate seed format
    if len(hex_seed) != 64:
        return

    try:
        # 2. Convert hex → bytes → base32
        seed_bytes = bytes.fromhex(hex_seed)
        base32_seed = base64.b32encode(seed_bytes).decode()

        # Generate TOTP
        totp = pyotp.TOTP(base32_seed)
        code = totp.now()

        # 3. Current UTC timestamp
        timestamp = datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")

        # 4. Output line (cron redirects stdout)
        print(f"{timestamp} - 2FA Code: {code}")

    except Exception:
        # Never crash cron
        return


if __name__ == "__main__":
    main()
