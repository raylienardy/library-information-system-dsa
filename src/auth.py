# src/auth.py
"""
Hashing dan verifikasi password menggunakan PBKDF2-HMAC-SHA256.
Format penyimpanan: "<salt_hex>:<dk_hex>"
"""
import binascii
import hashlib
import os


def hash_password(password: str) -> str:
    """Hash password dengan salt acak. Kembaliannya string 'salt:dk' (hex)."""
    if not isinstance(password, str):
        raise TypeError("password must be str")
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, 100_000)
    return binascii.hexlify(salt).decode() + ":" + binascii.hexlify(dk).decode()


def verify_password(stored: str, provided: str) -> bool:
    """
    Verifikasi apakah provided password cocok dengan stored hash.
    stored harus dalam format 'salthex:dkhex'.
    """
    try:
        salt_hex, dk_hex = stored.split(":")
    except Exception:
        return False
    salt = binascii.unhexlify(salt_hex)
    new_dk = hashlib.pbkdf2_hmac("sha256", provided.encode("utf-8"), salt, 100_000)
    return binascii.hexlify(new_dk).decode() == dk_hex
