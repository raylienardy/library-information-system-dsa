# src/services/user_service.py
"""
Service layer ringan untuk operasi user (register + login).
Menggunakan persistence.repo -> UserRepo dan auth.
"""

from persistence.repo import UserRepo
from models.user import User
from auth import hash_password, verify_password
from typing import Tuple, Optional

class UserExistsError(Exception):
    pass

class AuthError(Exception):
    pass

def register_user(username: str, password: str, role: str = "user") -> User:
    """
    Register user baru. Jika username sudah ada, raise UserExistsError.
    Mengembalikan objek User (dengan id).
    """
    username = username.strip()
    if not username or not password:
        raise ValueError("username dan password tidak boleh kosong")
    # cek ada atau tidak
    existing = UserRepo.get_by_username(username)
    if existing:
        raise UserExistsError(f"Username '{username}' sudah ada")
    uid = UserRepo.add(username, password, role)
    user = UserRepo.get_by_username(username)
    if not user:
        # sesuatu yang ganjil
        raise Exception("Gagal membuat user baru")
    return user

def login_user(username: str, password: str) -> User:
    """
    Verifikasi credential; bila benar kembalikan User; kalau salah raise AuthError.
    """
    if not username or not password:
        raise AuthError("username/password kosong")
    user = UserRepo.get_by_username(username)
    if not user:
        raise AuthError("User tidak ditemukan")
    if not verify_password(user.password_hash, password):
        raise AuthError("Password salah")
    return user
