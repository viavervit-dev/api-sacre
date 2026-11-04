import os
from pathlib import Path

from src.api.settings.parameters import api_parameters

# Bind de red
bind = f"{api_parameters.host}:{api_parameters.port}"

# Clase de worker ASGI de alto rendimiento
worker_class = "uvicorn.workers.UvicornWorker"

# Concurrencia y procesos de trabajo para arquitecturas asíncronas (FastAPI / ASGI)
# En ASGI asíncrono (I/O no bloqueante con event loop), la fórmula clásica '(CPU * 2) + 1'
# de servidores WSGI sincrónicos sobrecarga la CPU y multiplica excesivamente las conexiones
# del pool de PostgreSQL. Se utiliza el conteo de CPU efectivo (respetando cgroups/Docker).
_detected_cpus = getattr(os, "process_cpu_count", os.cpu_count)() or 1
default_workers = max(_detected_cpus, 2)
workers = api_parameters.workers if api_parameters.workers > 0 else default_workers

# Gestión de conexiones y tiempos de espera en transacciones de E-commerce
# En checkout y compras mayoristas, los flujos interactúan con pasarelas externas y SMTP.
worker_connections = 1000
timeout = 60
# Tiempo suficiente para que órdenes y enlaces en curso completen antes del reciclaje
graceful_timeout = 45
# Superior al idle timeout común de balanceadores (ALB 60s, Nginx 65s) para evitar 502s
keepalive = 65

# Prevención de fugas de memoria en procesos de larga duración (reinicio suave)
# Jitter aleatorio para evitar reinicios simultáneos de workers durante picos de venta
max_requests = 5000
max_requests_jitter = 500

# Estabilidad en contenedores Docker/Kubernetes:
# Emplea memoria compartida (/dev/shm) para los latidos del worker (heartbeat)
# evitando falsos reinicios por SIGKILL causados por latencia de I/O en disco.
shm_path = Path("/dev/shm")
if shm_path.exists() and shm_path.is_dir():
    worker_tmp_dir = "/dev/shm"

# Aislamiento de conexiones y transacciones en base de datos:
# NUNCA precargar la aplicación en el proceso maestro (preload_app=False).
# Cada worker debe inicializar su propio bucle de eventos y su pool asyncpg en su propio lifespan.
preload_app = False

# Seguridad y proxies inversos (Cloudflare, Nginx, AWS ALB, Traefik)
# Permite interpretar cabeceras X-Forwarded-For para capturar la IP real del cliente
forwarded_allow_ips = api_parameters.forwarded_allow_ips

# Protección contra ataques de denegación de servicio (Slowloris / HTTP Header Flooding)
limit_request_line = 4094
limit_request_fields = 100
limit_request_field_size = 8190

# Registro y observabilidad hacia stdout/stderr (estándar de contenedores de 12 factores)
# Registra el tiempo de respuesta %(L)ss para auditar latencia en catálogo y pasarela
accesslog = "-"
errorlog = "-"
loglevel = "debug" if api_parameters.debug else "info"
access_log_format = '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %(L)ss'
