from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
import os
import time

from decrypt_seed import decrypt_seed
from totp_create_check import generate_totp_code, verify_totp_code

SEED_PATH = "/data/seed.txt"

app = FastAPI()


# ---------------------------
# Endpoint 1: POST /decrypt-seed
# ---------------------------
@app.post("/decrypt-seed")
async def decrypt_seed_endpoint(request: Request):
    try:
        body = await request.json()
        encrypted_seed = body.get("encrypted_seed")

        if not encrypted_seed:
            raise Exception("Missing encrypted_seed")

        seed = decrypt_seed(encrypted_seed)

        os.makedirs("/data", exist_ok=True)
        with open(SEED_PATH, "w") as f:
            f.write(seed)

        return {"status": "ok"}

    except Exception:
        return JSONResponse(
            status_code=500,
            content={"error": "Decryption failed"}
        )


# ---------------------------
# Endpoint 2: GET /generate-2fa
# ---------------------------
@app.get("/generate-2fa")
def generate_2fa():
    if not os.path.exists(SEED_PATH):
        return JSONResponse(
            status_code=500,
            content={"error": "Seed not decrypted yet"}
        )

    try:
        with open(SEED_PATH, "r") as f:
            seed = f.read().strip()

        code, valid_for = generate_totp_code(seed)

        # Ensure valid_for is 0–29 (spec compliant)
        if valid_for == 30:
            valid_for = 0

        return {
            "code": code,
            "valid_for": valid_for
        }

    except Exception:
        return JSONResponse(
            status_code=500,
            content={"error": "Seed not decrypted yet"}
        )


# ---------------------------
# Endpoint 3: POST /verify-2fa
# ---------------------------
@app.post("/verify-2fa")
async def verify_2fa(request: Request):
    try:
        body = await request.json()
    except Exception:
        return JSONResponse(
            status_code=400,
            content={"error": "Missing code"}
        )

    code = body.get("code")
    if not code:
        return JSONResponse(
            status_code=400,
            content={"error": "Missing code"}
        )

    if not os.path.exists(SEED_PATH):
        return JSONResponse(
            status_code=500,
            content={"error": "Seed not decrypted yet"}
        )

    with open(SEED_PATH, "r") as f:
        seed = f.read().strip()

    is_valid = verify_totp_code(seed, code)
    return {"valid": is_valid}
