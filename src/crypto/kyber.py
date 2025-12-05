# src/crypto/kyber.py
from dataclasses import dataclass
from typing import Any, Dict
import oqs

from .base import CryptoKeyPair, CryptoScheme
from .aes_gcm import aes256_gcm_encrypt, aes256_gcm_decrypt


@dataclass
class KyberScheme(CryptoScheme):
    """
    Generic Kyber + AES-256-GCM wrapper.

    mechanism: "Kyber512", "Kyber768", etc
    name: string ID used in your experiments, e.g. "kyber768_aes256_gcm".
    """
    mechanism: str
    name: str

    def keygen(self) -> CryptoKeyPair:
        with oqs.KeyEncapsulation(self.mechanism) as kem:
            public_key = kem.generate_keypair()
            secret_key = kem.export_secret_key()
        # store raw bytes; we’ll re-create kem objects on use
        return CryptoKeyPair(public=public_key, private=secret_key)

    def encrypt(self, public_key: bytes, plaintext: bytes) -> Dict[str, Any]:
        # 1) KEM: derive shared secret using recipient public key
        with oqs.KeyEncapsulation(self.mechanism) as kem:
            kem_ct, shared_secret = kem.encap_secret(public_key)

        # 2) Use shared_secret (32 bytes) directly as AES-256 key
        nonce, ciphertext = aes256_gcm_encrypt(shared_secret, plaintext)

        return {
            "ciphertext": ciphertext,
            "nonce": nonce,
            "meta": {
                "kem_ciphertext": kem_ct,
            },
        }

    def decrypt(self, private_key: bytes, bundle: Dict[str, Any]) -> bytes:
        kem_ct = bundle["meta"]["kem_ciphertext"]
        nonce = bundle["nonce"]
        ciphertext = bundle["ciphertext"]

        # 1) Recreate KEM object using secret key bytes
        with oqs.KeyEncapsulation(self.mechanism, secret_key=private_key) as kem:
            shared_secret = kem.decap_secret(kem_ct)

        # 2) AES-GCM decrypt
        plaintext = aes256_gcm_decrypt(shared_secret, nonce, ciphertext)
        return plaintext


# Concrete scheme instances you can use:

kyber768_aes256_gcm = KyberScheme(
    mechanism="Kyber768",
    name="kyber768_aes256_gcm",
)

kyber512_aes256 = KyberScheme(
    mechanism="Kyber512",
    name="kyber512_aes256",
)
