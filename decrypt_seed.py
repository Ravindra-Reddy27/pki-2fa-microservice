import base64
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes, serialization


def load_private_key():
    with open("student_private.pem", "rb") as f:
        return serialization.load_pem_private_key(
            f.read(),
            password=None
        )


def decrypt_seed(encrypted_seed_b64: str) -> str:
    private_key = load_private_key()

    encrypted_bytes = base64.b64decode(encrypted_seed_b64)

    decrypted_bytes = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )

    seed = decrypted_bytes.decode("utf-8")

    if len(seed) != 64 or not all(c in "0123456789abcdef" for c in seed):
        raise ValueError("Invalid seed format")

    return seed
