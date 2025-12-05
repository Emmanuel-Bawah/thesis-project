# src/crypto/base.py
from dataclasses import dataclass
from typing import Any, Protocol


@dataclass
class CryptoKeyPair:
    public: Any
    private: Any


class CryptoScheme(Protocol):
    name: str

    def keygen(self) -> CryptoKeyPair:
        ...

    def encrypt(self, public_key: Any, plaintext: bytes) -> dict:
        """
        Returns a dict that contains everything needed to decrypt:
        {
            "ciphertext": bytes,
            "nonce": bytes,
            "meta": {...}  # scheme-specific extra (kem_ct, encrypted_key, eph_pub, etc.)
        }
        """
        ...

    def decrypt(self, private_key: Any, bundle: dict) -> bytes:
        ...
