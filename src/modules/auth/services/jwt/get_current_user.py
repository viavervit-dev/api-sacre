from src.modules.auth.dto import ReadUserDTO
from src.modules.auth.models.user import User


class RetrieveCurrentUserService:
    """Servicio encargado de formatear la información del usuario autenticado actual."""

    @classmethod
    async def get_current_user(cls, instance: User) -> ReadUserDTO:
        """Construye el DTO con los datos del usuario autenticado en la sesión."""

        role = instance.role
        profile_instance = getattr(instance, role)

        return ReadUserDTO.model_construct(
            id=instance.id,
            first_names=profile_instance.first_names,
            last_names=profile_instance.last_names,
            email=instance.email,
            role=role,
        )
