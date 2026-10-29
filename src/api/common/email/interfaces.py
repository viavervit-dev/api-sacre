from abc import ABC, abstractmethod


class IEmailService(ABC):
    """Contrato de interfaz para el envío de correos electrónicos."""

    @abstractmethod
    async def send_email(
        self,
        recipient: str,
        subject: str,
        html_content: str,
        text_content: str,
    ) -> None:
        """
        Envía un correo electrónico de forma asíncrona.

        Args:
            recipient: Dirección de correo electrónico del destinatario.
            subject: Asunto del correo.
            html_content: Contenido principal en formato HTML.
            text_content: Contenido alternativo en texto plano para clientes sin soporte HTML
                y mitigación de filtros anti-spam.
        """

        pass
