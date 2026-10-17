"""aqui lo que estaba haciendo es el envío de correos con smtplib (que seria librería estándar)."""
import smtplib
from email.message import EmailMessage

from ..config import OTP_EXPIRE_MINUTES, SMTP_HOST, SMTP_PASSWORD, SMTP_PORT, SMTP_USER


class EmailError(Exception):
    """No se pudo enviar el correo."""


def send_otp_email(to_email: str, code: str) -> None:
    """Recordatorio: tener en cuenta el porque , se Envía el código OTP al correo del usuario. y luego Lanza EmailError si falla."""
    msg = EmailMessage()
    msg["Subject"] = "Tu código de verificación"
    msg["From"] = SMTP_USER
    msg["To"] = to_email
    msg.set_content(
        f"Tu código de verificación es: {code}\n"
        f"Es válido por {OTP_EXPIRE_MINUTES} minutos. Si no lo solicitaste, ignora este mensaje."
    )
    try:
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT, timeout=15) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
    except (smtplib.SMTPException, OSError) as exc:
      
        raise EmailError("No se pudo enviar el correo") from exc
    
  