import asyncio
import logging
import smtplib
import ssl
from email.message import EmailMessage
from email.utils import formataddr

import certifi

from src.api.common.email.constants import ExceptionErrorMessages as EmailException
from src.api.common.exceptions import EmailConfigurationError, EmailDeliveryError

logger = logging.getLogger(__name__)


class EmailService:
    """Servicio encargado del envío asíncrono de correos electrónicos mediante SMTP (SSL/TLS)."""

    def __init__(
        self,
        server: str,
        port: int,
        username: str,
        password: str,
        from_name: str = "Sacré",
        from_address: str = "",
        use_ssl: bool = True,
        starttls: bool = False,
        timeout: int = 15,
    ) -> None:
        self.__server = server
        self.__port = port
        self.__username = username
        self.__password = password
        self.__from_name = from_name
        self.__from_address = from_address or username
        self.__use_ssl = use_ssl
        self.__starttls = starttls
        self.__timeout = timeout

    async def send_email(
        self,
        recipient: str,
        subject: str,
        html_content: str,
        text_content: str,
    ) -> None:
        """
        Construye y envía un correo electrónico multipart (texto plano y HTML) de forma
        asíncrona mediante un pool de hilos con control de timeout.

        Raises:
            EmailConfigurationError: Si faltan las credenciales o falla la autenticación SMTP.
            EmailDeliveryError: Si ocurre un fallo de conexión, red o se agota el timeout.
        """

        if not self.__username or not self.__password:
            raise EmailConfigurationError(
                message=EmailException.CREDENTIALS_NOT_CONFIGURED.value,
            )

        message = EmailMessage()
        message["Subject"] = subject
        message["From"] = formataddr(pair=(self.__from_name, self.__from_address))
        message["To"] = recipient

        # Fallback de texto plano para clientes sin soporte HTML y prevención de spam
        message.set_content(text_content, charset="utf-8")
        message.add_alternative(html_content, subtype="html", charset="utf-8")

        # Configuración estricta de contexto TLS con autoridades de certificación verificadas
        ssl_context = ssl.create_default_context(cafile=certifi.where())

        def __send() -> None:
            """
            Establece la conexión con el servidor SMTP, autentica y envía el mensaje de correo.

            Raises:
                EmailConfigurationError: Si fallan las credenciales de autenticación SMTP.
                EmailDeliveryError: Si ocurre un error de conexión, timeout o fallo de red.
            """

            try:
                if self.__use_ssl:
                    with smtplib.SMTP_SSL(
                        host=self.__server,
                        port=self.__port,
                        context=ssl_context,
                        timeout=self.__timeout,
                    ) as server:
                        server.login(user=self.__username, password=self.__password)
                        server.send_message(msg=message)
                else:
                    with smtplib.SMTP(
                        host=self.__server,
                        port=self.__port,
                        timeout=self.__timeout,
                    ) as server:
                        if self.__starttls:
                            server.starttls(context=ssl_context)

                        server.login(user=self.__username, password=self.__password)
                        server.send_message(msg=message)
            except smtplib.SMTPAuthenticationError as exc:
                logger.critical("Error de autenticación SMTP.")

                raise EmailConfigurationError(
                    message=EmailException.AUTHENTICATION_ERROR.value,
                ) from exc
            except (
                smtplib.SMTPConnectError,
                smtplib.SMTPServerDisconnected,
            ) as exc:
                logger.error("Error de conexión o timeout con el servidor SMTP: %s", exc)

                raise EmailDeliveryError(
                    message=EmailException.CONNECTION_ERROR.value,
                ) from exc
            except OSError as exc:
                logger.error("Error de socket o red a nivel de sistema operativo: %s", exc)

                raise EmailDeliveryError(
                    message=EmailException.CONNECTION_ERROR.value,
                ) from exc

        total_timeout = min(max(self.__timeout * 2, 25), 35)

        try:
            async with asyncio.timeout(total_timeout):
                await asyncio.to_thread(__send)
        except TimeoutError as exc:
            logger.error("Tiempo máximo total agotado al enviar correo SMTP: %s", exc)

            raise EmailDeliveryError(
                message=EmailException.CONNECTION_ERROR.value,
            ) from exc
