# Sistema de Autenticación con OTP (FastAPI)

Parcial de Desarrollo de Software. API de autenticación con registro, login,
código OTP de 6 dígitos enviado por correo (válido 15 minutos) y tokens JWT.

- **Autor:** (tu nombre completo)
- **Despliegue:** https://TU-SERVICIO.onrender.com/docs
- **Repositorio:** https://github.com/Adolgil/Parcial-otp

## Stack

- FastAPI (Python 3.13)
- SQLAlchemy + SQLite
- PyOTP (generación de OTP)
- bcrypt (hash de contraseñas)
- python-jose (JWT)
- smtplib (envío de correo)
- pytest

## Estructura

```
app/
  main.py            aplicación principal y manejo de errores
  config.py          variables de entorno
  database.py        conexión SQLite
  models.py          users, otp_codes, login_sessions
  schemas.py         esquemas Pydantic
  security.py        bcrypt y JWT
  middleware.py      validación de tokens
  routes/            auth.py, users.py
  services/          email_service.py, otp_service.py
tests/
```

## Instalación local

```
git clone https://github.com/Adolgil/Parcial-otp.git
cd Parcial-otp
python -m venv venv
venv\Scripts\activate          # Linux/Mac: source venv/bin/activate
pip install -r requirements.txt
```

Crea un archivo `.env` en la raíz:

```
SECRET_KEY=una-clave-larga-y-aleatoria
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
OTP_EXPIRE_MINUTES=15
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=tucorreo@gmail.com
SMTP_PASSWORD=contraseña-de-aplicación
```

Para Gmail se necesita la verificación en dos pasos y una contraseña de aplicación.

## Ejecución

```
uvicorn app.main:app --reload
```

Documentación interactiva en http://127.0.0.1:8000/docs

## Endpoints

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| POST | /auth/register | Registrar usuario | No |
| POST | /auth/login | Validar credenciales y enviar OTP | No |
| POST | /auth/resend-otp | Reenviar OTP | No |
| POST | /auth/verify-otp | Verificar OTP y obtener JWT | No |
| POST | /auth/refresh | Refrescar token | Sí |
| POST | /auth/logout | Cerrar sesión y revocar token | Sí |
| GET | /users/profile | Ver perfil | Sí |
| PUT | /users/profile | Actualizar perfil | Sí |

Estado: (indica cuáles están implementadas y cuáles pendientes).

## Seguridad

- Contraseñas hasheadas con bcrypt (salt por usuario).
- Validación de contraseña: mínimo 8 caracteres, letras y números.
- OTP de 6 dígitos, válido 15 minutos y de un solo uso; al generar uno nuevo se invalidan los anteriores.
- Comparación del OTP en tiempo constante.
- JWT con claims `sub`, `iat`, `exp` y `jti`.
- Los errores de login no revelan si el usuario existe.
- Los errores de validación no devuelven el valor enviado (no se filtran contraseñas).
- Secretos en variables de entorno; `.env` no se versiona.

## Base de datos

Tablas: `users`, `otp_codes` y `login_sessions`. El logout elimina la fila de
`login_sessions`; un token solo es válido si existe ahí.

## Pruebas

```
pytest
```

(Indica cuántos tests unitarios y de integración tienes.)

## Despliegue en Render

- Build: `pip install -r requirements.txt`
- Start: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
- Variables de entorno configuradas en el panel de Render.

### Limitaciones conocidas

- **Correo en producción:** el plan gratuito de Render bloquea el tráfico saliente a los
  puertos SMTP 25, 465 y 587 (cambio de septiembre de 2025). El envío de OTP funciona
  en local con Gmail, pero en Render `login` responde 503. Se resolvería con una
  instancia de pago o con un proveedor de correo por HTTP o por el puerto 2525.
- **Base de datos:** el disco del plan gratuito es temporal, por lo que los datos de
  SQLite se pierden al reiniciar o redesplegar el servicio.