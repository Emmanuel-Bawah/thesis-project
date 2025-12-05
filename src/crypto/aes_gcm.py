# src/crypto/aes_gcm.py
import os
from typing import Tuple, Optional
from cryptography.hazmat.primitives.ciphers.aead import AESGCM


def aes256_gcm_encrypt(key: bytes, plaintext: bytes, aad: Optional[bytes] = None) -> Tuple[bytes, bytes]:
    """
    AES-256-GCM encryption helper.
    - key: 32 bytes
    - returns (nonce, ciphertext)
    """
    if len(key) != 32:
        raise ValueError("AES-256-GCM key must be 32 bytes")

    nonce = os.urandom(12)  # GCM standard nonce size
    aesgcm = AESGCM(key)
    ciphertext = aesgcm.encrypt(nonce, plaintext, aad)
    return nonce, ciphertext


def aes256_gcm_decrypt(key: bytes, nonce: bytes, ciphertext: bytes, aad: Optional[bytes] = None) -> bytes:
    """
    AES-256-GCM decryption helper.
    """
    if len(key) != 32:
        raise ValueError("AES-256-GCM key must be 32 bytes")

    aesgcm = AESGCM(key)
    return aesgcm.decrypt(nonce, ciphertext, aad)
