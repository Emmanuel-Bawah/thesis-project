# tests/test_crypto_core.py
import oqs
print(f"DEBUG: oqs file location: {oqs.__file__}")
print(f"DEBUG: oqs attributes: {dir(oqs)}")

from src.crypto import get_scheme

PLAINTEXT = b"Hello, this is a test message for my MSc thesis experiments."


def round_trip(name: str):
    scheme = get_scheme(name)
    kp = scheme.keygen()
    bundle = scheme.encrypt(kp.public, PLAINTEXT)
    recovered = scheme.decrypt(kp.private, bundle)
    assert recovered == PLAINTEXT
    print(f"[OK] {name} round-trip works")


if __name__ == "__main__":
    for scheme_name in [
        "kyber768_aes256_gcm",
        "kyber512_aes256",
        "rsa2048_aes256",
        "ecdh_p256_aes256",
    ]:
        round_trip(scheme_name)
