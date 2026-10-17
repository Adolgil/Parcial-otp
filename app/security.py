"""Utilidades de seguridad: se encuentra el hashing de contraseñas con bcrypt."""
import bcrypt


def hash_password(password: str) -> str:
    """Devuelve el hash bcrypt (con salt incluido) de la contraseña."""
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")


def verify_password(password: str, password_hash: str) -> bool:
    """Compara una contraseña en texto plano contra su hash."""
    try:
        return bcrypt.checkpw(password.encode("utf-8"), password_hash.encode("utf-8"))
    except ValueError:
        return False