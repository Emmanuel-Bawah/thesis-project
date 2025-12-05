# src/crypto/ecdh.py
import os
from dataclasses import dataclass
from typing import Any, Dict

from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.primitives.serialization import (
    Encoding,
    PublicFormat,
)
from cryptography.hazmat.primitives.kdf.hkdf import HKDF
from cryptography.hazmat.primitives import hashes

from cryptography.hazmat.primitives.asymmetric.ec import (
    EllipticCurvePublicKey,
)

from .base import CryptoKeyPair, CryptoScheme
from .aes_gcm import aes256_gcm_encrypt, aes256_gcm_decrypt


def _kdf_256(shared_secret: bytes) -> bytes:
    """Derive a 32-byte AES key from ECDH shared secret."""
    hkdf = HKDF(
        algorithm=hashes.SHA256(),
        length=32,
        salt=None,
        info=b"ecdh_p256_aes256",
    )
    return hkdf.derive(shared_secret)


@dataclass
class ECDHP256AES256(CryptoScheme):
    name: str = "ecdh_p256_aes256"

    def keygen(self) -> CryptoKeyPair:
        private_key = ec.generate_private_key(ec.SECP256R1())
        public_key = private_key.public_key()
        return CryptoKeyPair(public=public_key, private=private_key)

    def encrypt(self, public_key: EllipticCurvePublicKey, plaintext: bytes) -> Dict[str, Any]:
        # 1) Generate ephemeral key pair
        eph_private_key = ec.generate_private_key(ec.SECP256R1())
        eph_public_key = eph_private_key.public_key()

        # 2) ECDH shared secret with receiver's static public key
        shared_secret = eph_private_key.exchange(ec.ECDH(), public_key)
        aes_key = _kdf_256(shared_secret)

        # 3) AES-GCM encrypt
        nonce, ciphertext = aes256_gcm_encrypt(aes_key, plaintext)

        # 4) Serialize ephemeral public key so receiver can reconstruct it
        eph_public_bytes = eph_public_key.public_bytes(
            encoding=Encoding.X962,
            format=PublicFormat.UncompressedPoint,
        )

        return {
            "ciphertext": ciphertext,
            "nonce": nonce,
            "meta": {
                "eph_public": eph_public_bytes,
            },
        }

    def decrypt(self, private_key: Any, bundle: Dict[str, Any]) -> bytes:
        eph_public_bytes = bundle["meta"]["eph_public"]
        nonce = bundle["nonce"]
        ciphertext = bundle["ciphertext"]

        # 1) Rebuild ephemeral public key
        eph_public_key = EllipticCurvePublicKey.from_encoded_point(
            ec.SECP256R1(),
            eph_public_bytes,
        )

        # 2) ECDH shared secret with receiver's static private key
        shared_secret = private_key.exchange(ec.ECDH(), eph_public_key)
        aes_key = _kdf_256(shared_secret)

        # 3) AES-GCM decrypt
        plaintext = aes256_gcm_decrypt(aes_key, nonce, ciphertext)
        return plaintext


ecdh_p256_aes256 = ECDHP256AES256()
