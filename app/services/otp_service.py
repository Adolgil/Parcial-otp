"""Generación de códigos OTP de 6 dígitos con PyOTP."""
import secrets
from datetime import timedelta

import pyotp
from sqlalchemy.orm import Session

from ..config import OTP_EXPIRE_MINUTES
from ..models import OTPCode, User, utcnow


def _random_code() -> str:
    """Código de 6 dígitos a partir de un secreto aleatorio y un contador impredecible."""
    hotp = pyotp.HOTP(pyotp.random_base32(), digits=6)
    return hotp.at(secrets.randbelow(10**9))


def generate_otp(db: Session, user: User) -> str:
    """Invalida los OTP anteriores del usuario, crea uno nuevo y lo devuelve."""
    db.query(OTPCode).filter(
        OTPCode.user_id == user.id, OTPCode.used == False  # noqa: E712
    ).update({"used": True})

    code = _random_code()
    db.add(OTPCode(
        user_id=user.id,
        code=code,
        expires_at=utcnow() + timedelta(minutes=OTP_EXPIRE_MINUTES),
    ))
    db.commit()
    return code