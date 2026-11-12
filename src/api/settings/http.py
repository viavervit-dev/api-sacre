import certifi
import httpx

from src.api.settings.parameters import api_parameters

# Instancia global del cliente
_http_client: httpx.AsyncClient | None = None


async def create_http_client() -> None:
    """
    Inicializa el cliente HTTP asíncrono con pool de conexiones y timeouts.
    Se ejecuta al iniciar la aplicación en el lifespan.
    """

    global _http_client

    # Configuración de límites del pool y tiempos de espera
    limits = httpx.Limits(
        max_connections=100,  # Conexiones simultáneas máximas
        max_keepalive_connections=50,  # Conexiones inactivas mantenidas vivas en el pool
        keepalive_expiry=30.0,  # Segundos que una conexión se mantiene viva
    )

    # Configuración de timeouts granulares y estrictos
    timeout = httpx.Timeout(
        connect=5.0,  # Handshake TCP/TLS rápido
        read=10.0,  # Espera razonable para procesamiento bancario
        write=5.0,  # Envío rápido del payload
        pool=5.0,  # Falla rápido si no hay conexiones libres en el pool
    )

    # Configuración de cabeceras base seguras
    headers = {
        "User-Agent": f"{api_parameters.app_name}/{api_parameters.app_version}",
        "Accept": "application/json",
    }

    # Configuración de AsyncClient
    _http_client = httpx.AsyncClient(
        limits=limits,
        timeout=timeout,
        headers=headers,
        verify=certifi.where(),
        follow_redirects=False,
    )


async def close_http_client() -> None:
    """Cierra el cliente y libera las conexiones activas en el shutdown."""

    global _http_client

    if _http_client is not None:
        await _http_client.aclose()
        _http_client = None


def http_client() -> httpx.AsyncClient:
    """Dependencia para inyectar la instancia compartida de `httpx.AsyncClient`."""

    if _http_client is None:
        raise RuntimeError(
            "El cliente HTTP no ha sido inicializado. "
            "Asegúrate de invocar 'create_http_client' en el lifespan."
        )

    return _http_client
