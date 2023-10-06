import base64
import hashlib


# Funkcja do haszowania hasła
def HashPassword(password):
    hashed_bytes = hashlib.sha256(password.encode()).digest()
    hashed_password = base64.b64encode(hashed_bytes).decode()
    return hashed_password
