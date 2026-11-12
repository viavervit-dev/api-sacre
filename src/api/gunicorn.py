import os
from pathlib import Path

from src.api.settings.parameters import api_parameters

# Bind de red
bind = f"{api_parameters.host}:{api_parameters.port}"

# Clase de worker ASGI de alto rendimiento
worker_class = "uvicorn.workers.UvicornWorker"

# Concurrencia y procesos de trabajo para arquitecturas asíncronas (FastAPI / ASGI)
# Conviene configurar la variable WORKERS explícitamente en el entorno de producción,
# ya que os.process_cpu_count() lee afinidad de núcleos del host y no cuotas CFS de cgroups/Docker.
_detected_cpus = getattr(os, "process_cpu_count", os.cpu_count)() or 1
default_workers = max(_detected_cpus, 2)
workers = api_parameters.workers if api_parameters.workers > 0 else default_workers

# Tiempos de espera y ciclo de vida del proceso
# timeout: tiempo máximo de silencio/heartbeat del worker antes de que el master lo reinicie
# (no cancela peticiones HTTP individuales; el timeout de I/O se controla en la aplicación).
timeout = 60

# graceful_timeout: tiempo de espera para que solicitudes en curso finalicen al detener el worker
# (requiere configurar el tiempo de parada del contenedor en al menos 50s antes de enviar SIGKILL).
graceful_timeout = 45

# keepalive: tiempo para conexiones inactivas, superior al idle timeout del proxy.
keepalive = 65

# Prevención de fugas de memoria en procesos de larga duración (reinicio suave)
# Jitter aleatorio para evitar reinicios simultáneos de workers durante picos de tráfico
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

# Registro y observabilidad hacia stdout/stderr (estándar de contenedores de 12 factores)
# Uvicorn gestiona su propio formateador de acceso; los tiempos de respuesta deben medirse
# en el proxy inverso (ej. $request_time en Nginx) o mediante middleware ASGI.
accesslog = "-"
errorlog = "-"
loglevel = "debug" if api_parameters.debug else "info"
