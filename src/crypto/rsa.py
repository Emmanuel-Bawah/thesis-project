# src/crypto/rsa.py
import os
from dataclasses import dataclass
from typing import Any, Dict

from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes

from .base import CryptoKeyPair, CryptoScheme
from .aes_gcm import aes256_gcm_encrypt, aes256_gcm_decrypt


@dataclass
class RSA2048AES256(CryptoScheme):
    name: str = "rsa2048_aes256"

    def keygen(self) -> CryptoKeyPair:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
        )
        public_key = private_key.public_key()
        return CryptoKeyPair(public=public_key, private=private_key)

    def encrypt(self, public_key: Any, plaintext: bytes) -> Dict[str, Any]:
        # 1) Generate random AES-256 key
        aes_key = os.urandom(32)

        # 2) Encrypt AES key with RSA-OAEP
        encrypted_key = public_key.encrypt(
            aes_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        # 3) Encrypt data with AES-GCM
        nonce, ciphertext = aes256_gcm_encrypt(aes_key, plaintext)

        return {
            "ciphertext": ciphertext,
            "nonce": nonce,
            "meta": {
                "encrypted_key": encrypted_key,
            },
        }

    def decrypt(self, private_key: Any, bundle: Dict[str, Any]) -> bytes:
        encrypted_key = bundle["meta"]["encrypted_key"]
        nonce = bundle["nonce"]
        ciphertext = bundle["ciphertext"]

        # 1) Recover AES key using RSA private key
        aes_key = private_key.decrypt(
            encrypted_key,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None,
            ),
        )

        # 2) AES-GCM decrypt
        plaintext = aes256_gcm_decrypt(aes_key, nonce, ciphertext)
        return plaintext


rsa2048_aes256 = RSA2048AES256()
