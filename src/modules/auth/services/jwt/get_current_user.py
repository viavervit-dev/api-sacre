from src.modules.admins.models.admin import Admin
from src.modules.auth.dto import CurrentUserDTO
from src.modules.customers.models.customer import Customer


class GetCurrentUserService:
    """Servicio para obtener la información del usuario actual de la sesión."""

    async def get_current_user(self, instance: Admin | Customer) -> CurrentUserDTO:
        """Obtiene la información del usuario actual de la sesión."""

        return CurrentUserDTO.model_construct(**instance.__dict__)
