# src/crypto/__init__.py
from typing import Dict

from .kyber import kyber768_aes256_gcm, kyber512_aes256
from .rsa import rsa2048_aes256
from .ecdh import ecdh_p256_aes256
from .base import CryptoScheme

_SCHEMES: Dict[str, CryptoScheme] = {
    kyber768_aes256_gcm.name: kyber768_aes256_gcm,
    kyber512_aes256.name: kyber512_aes256,
    rsa2048_aes256.name: rsa2048_aes256,
    ecdh_p256_aes256.name: ecdh_p256_aes256,
}


def get_scheme(name: str) -> CryptoScheme:
    return _SCHEMES[name]


__all__ = [
    "get_scheme",
    "kyber768_aes256_gcm",
    "kyber512_aes256",
    "rsa2048_aes256",
    "ecdh_p256_aes256",
]
