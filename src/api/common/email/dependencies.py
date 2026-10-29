from functools import lru_cache

from src.api.common.email.service import EmailService
from src.api.settings.parameters import api_parameters


@lru_cache
def email_service() -> EmailService:
    """Provee una instancia singleton del servicio de correo electrónico."""

    return EmailService(
        server=api_parameters.mail_server,
        port=api_parameters.mail_port,
        username=api_parameters.mail_username,
        password=api_parameters.mail_password,
        from_name="Sacré",
        from_address=api_parameters.mail_from_address or api_parameters.mail_username,
        use_ssl=api_parameters.mail_use_ssl,
        starttls=api_parameters.mail_starttls,
        timeout=api_parameters.mail_timeout,
    )
