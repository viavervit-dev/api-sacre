from enum import Enum


class ExceptionErrorMessages(Enum):
    """
    Enumeración que define constantes relacionadas con los mensajes de error para excepciones
    del servicio de correo electrónico.
    """

    CREDENTIALS_NOT_CONFIGURED = "Credenciales del servidor de correo no configuradas."
    AUTHENTICATION_ERROR = "Error de autenticación con el servidor de correo."
    CONNECTION_ERROR = "No fue posible conectar con el servidor de correo. Intente más tarde."
