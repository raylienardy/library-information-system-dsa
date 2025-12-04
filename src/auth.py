# src/auth.py
import os, hashlib, binascii
from typing import Tuple

def hash_password(password: str) -> str:
    """Hash password menggunakan PBKDF2-HMAC-SHA256.
    Format return: salthex:dkhex
    """
    salt = os.urandom(16)
    dk = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100_000)
    return binascii.hexlify(salt).decode() + ':' + binascii.hexlify(dk).decode()

def verify_password(stored: str, provided: str) -> bool:
    """Verifikasi password: bandingkan PBKDF2 dari provided dengan stored."""
    try:
        salt_hex, dk_hex = stored.split(':')
    except ValueError:
        return False
    salt = binascii.unhexlify(salt_hex)
    new_dk = hashlib.pbkdf2_hmac('sha256', provided.encode('utf-8'), salt, 100_000)
    return binascii.hexlify(new_dk).decode() == dk_hex
