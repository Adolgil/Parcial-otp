"""como se logra apreciar estos son los esquemas Pydantic que sirven para validar entradas y dar forma a las respuestas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator


def _validar_password(v: str) -> str:
    """Mínimo 8 caracteres, con letra y número; máximo 72 bytes (límite de bcrypt)."""
    if len(v) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres")
    if len(v.encode("utf-8")) > 72:
        raise ValueError("La contraseña es demasiado larga (máximo 72 bytes)")
    if not any(c.isalpha() for c in v) or not any(c.isdigit() for c in v):
        raise ValueError("La contraseña debe contener letras y números")
    return v


class UserCreate(BaseModel):
    """los datos para registrar un usuario."""
    email: EmailStr
    password: str
    full_name: str = Field(min_length=2, max_length=100)

    model_config = ConfigDict(json_schema_extra={
        "example": {"email": "ana@correo.com", "password": "Clave1234", "full_name": "Ana Pérez"}
    })

    @field_validator("password")
    @classmethod
    def password_valida(cls, v: str) -> str:
        return _validar_password(v)


class UserLogin(BaseModel):
    """en esta estan las credenciales de login."""
    email: EmailStr
    password: str

    model_config = ConfigDict(json_schema_extra={
        "example": {"email": "ana@correo.com", "password": "Clave1234"}
    })


class OTPVerify(BaseModel):
    """despues se hace la verificación del código OTP de 6 dígitos."""
    email: EmailStr
    code: str = Field(pattern=r"^\d{6}$")

    model_config = ConfigDict(json_schema_extra={
        "example": {"email": "ana@correo.com", "code": "123456"}
    })


class OTPResend(BaseModel):
    """Solicitud de reenvío de OTP."""
    email: EmailStr


class Token(BaseModel):
    """Respuesta con el JWT."""
    access_token: str
    token_type: str = "bearer"


class UserOut(BaseModel):
    """Datos públicos del usuario (nunca incluye el hash)."""
    id: int
    email: EmailStr
    full_name: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    """Campos que se pueden actualizar en el perfil."""
    full_name: Optional[str] = Field(default=None, min_length=2, max_length=100)
    password: Optional[str] = None

    @field_validator("password")
    @classmethod
    def password_valida(cls, v: Optional[str]) -> Optional[str]:
        return _validar_password(v) if v is not None else v


class MessageOut(BaseModel):
    """Respuesta simple con un mensaje."""
    message: str
    
    