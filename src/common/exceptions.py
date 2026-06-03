class AuthenticationFailed(Exception):
    """Excepción para fallos de las opciones de autenticación de la aplicación."""

    pass


class ResourceNotFound(Exception):
    """Excepción para recursos no encontrados."""

    pass


class UserNotFound(Exception):
    """Excepción para cuando un usuario no es encontrado en la base de datos."""

    pass


class MissingJWT(Exception):
    """
    Excepción para solicitudes que requieren autenticación JWT pero no incluyen los tokens
    necesarios.
    """

    pass


class PermissionDenied(Exception):
    """
    Excepción para solicitudes donde el usuario autenticado no tiene los permisos necesarios.
    """

    pass
