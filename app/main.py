"""Aplicación principal FastAPI: sistema de autenticación con OTP."""
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from . import models  # noqa: F401  (registra los modelos en Base.metadata)
from .database import Base, engine
from .routes import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Sistema de Autenticación con OTP", version="1.0.0")


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Devuelve errores de validación sin el valor enviado (evita filtrar contraseñas)."""
    errors = [{"loc": e["loc"], "msg": e["msg"]} for e in exc.errors()]
    return JSONResponse(status_code=422, content={"detail": errors})


app.include_router(auth.router)


@app.get("/", tags=["Estado"])
def root():
    """Comprobación de que el servicio está activo."""
    return {"status": "ok"}