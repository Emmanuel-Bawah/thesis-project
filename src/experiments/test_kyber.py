from src.crypto.schemes import get_scheme_by_name

def test_scheme(name: str):
    scheme = get_scheme_by_name(name)
    plaintext = b'{"amount": 10.5, "device": "low_end", "network": "3G"}'

    (pub, priv), keygen_metrics = scheme.keygen()
    enc_result = scheme.encrypt(plaintext, pub)
    ct = enc_result.ciphertext
    enc_metrics = enc_result.extra

    pt_out, dec_metrics = scheme.decrypt(ct, priv)

    print(f"Scheme: {name}")
    print("Keygen:", keygen_metrics)
    print("Encrypt:", enc_metrics)
    print("Decrypt:", dec_metrics)
    print("Plaintext OK?:", pt_out == plaintext)

if __name__ == "__main__":
    test_scheme("rsa2048_aes256")
    test_scheme("ecdh_p256_aes256")
    test_scheme("kyber512_aes256")
    test_scheme("kyber768_aes256_gcm")
