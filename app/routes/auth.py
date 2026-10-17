"""Endpoints de autenticación."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas import MessageOut, OTPResend, UserCreate, UserLogin, UserOut
from ..security import hash_password, verify_password
from ..services.email_service import EmailError, send_otp_email
from ..services.otp_service import generate_otp

router = APIRouter(prefix="/auth", tags=["Autenticación"])

OTP_SENT = "Si las credenciales son correctas, se envió un código al correo"


def _issue_otp(db: Session, user: User) -> None:
    """Genera el OTP y lo envía; si el correo falla responde 503."""
    code = generate_otp(db, user)
    try:
        send_otp_email(user.email, code)
    except EmailError:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "No se pudo enviar el código")


@router.post(
    "/register",
    response_model=UserOut,
    status_code=status.HTTP_201_CREATED,
    responses={409: {"description": "El email ya está registrado"}},
)
def register(data: UserCreate, db: Session = Depends(get_db)):
    """Registra un usuario nuevo. El email se normaliza a minúsculas y debe ser único."""
    email = data.email.lower()
    if db.query(User).filter(User.email == email).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "El email ya está registrado")

    user = User(
        email=email,
        password_hash=hash_password(data.password),
        full_name=data.full_name.strip(),
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.post("/login", response_model=MessageOut)
def login(data: UserLogin, db: Session = Depends(get_db)):
    """Valida usuario y contraseña y envía un OTP por correo."""
    user = db.query(User).filter(User.email == data.email.lower()).first()
    # Mismo mensaje para usuario inexistente o contraseña errónea (evita enumerar usuarios)
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Credenciales inválidas")
    _issue_otp(db, user)
    return {"message": OTP_SENT}


@router.post("/resend-otp", response_model=MessageOut)
def resend_otp(data: OTPResend, db: Session = Depends(get_db)):
    """Reenvía un OTP nuevo. Responde igual exista o no el usuario."""
    user = db.query(User).filter(User.email == data.email.lower()).first()
    if user:
        _issue_otp(db, user)
    return {"message": "Si el correo está registrado, se envió un nuevo código"}