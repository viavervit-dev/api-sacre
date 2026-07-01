from typing import Any


class BaseAppException(Exception):
    """Clase base para manejar datos dinámicos en las excepciones de la app."""

    def __init__(self, message: str, data: dict[str, Any] = {}) -> None:  # noqa
        self.message = message
        self.data = data
        super().__init__(self.message)


class AuthenticationFailed(BaseAppException):
    """Cuando no se logra autenticar un usuario."""

    pass


class ResourceNotFound(BaseAppException):
    """El recurso solicitado en la petición no existe."""

    pass


class UserNotFound(BaseAppException):
    """Cuando un usuario no existe."""

    pass


class MissingJWT(BaseAppException):
    """Cuando no se encuentran las cookies de JWT en la petición."""

    pass


class InvalidJWT(BaseAppException):
    """Cuando se proporciona un token JWT inválido."""

    pass


class PermissionDenied(BaseAppException):
    """Cuando un usuario autenticado no tiene los permisos necesarios."""

    pass


class DomainRuleViolation(BaseAppException):
    """Cuando se violan una regla de dominio."""

    pass
