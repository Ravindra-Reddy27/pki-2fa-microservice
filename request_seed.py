import requests
import json

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

STUDENT_ID = "24P35A0530"
GITHUB_REPO_URL = "https://github.com/Ravindra-Reddy27/pki-2fa-microservice"


def request_seed(student_id: str, github_repo_url: str, api_url: str):
    # 1. Read public key
    with open("student_public.pem", "r") as f:
        public_key = f.read()

    # 2. Prepare payload
    payload = {
        "student_id": student_id,
        "github_repo_url": github_repo_url,
        "public_key": public_key
    }

    # 3. Send request
    response = requests.post(
        api_url,
        headers={"Content-Type": "application/json"},
        data=json.dumps(payload),
        timeout=30
    )

    # 4. Handle response
    if response.status_code != 200:
        raise Exception(f"API Error {response.status_code}: {response.text}")

    data = response.json()

    if data.get("status") != "success":
        raise Exception(f"API returned error: {data}")

    encrypted_seed = data.get("encrypted_seed")
    if not encrypted_seed:
        raise Exception("Encrypted seed missing in response")

    # 5. Save encrypted seed (DO NOT COMMIT THIS FILE)
    with open("encrypted_seed.txt", "w") as f:
        f.write(encrypted_seed)

    print("Encrypted seed saved to encrypted_seed.txt")


if __name__ == "__main__":
    request_seed(STUDENT_ID, GITHUB_REPO_URL, API_URL)
