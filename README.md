<div>
    <img src="/assets/ProjectBanner.webp">
</div>

## 🔹 1. API Sacré

El sistema Sacré será una tienda virtual disponible inicialmente en **Ecuador**. Su propósito es ofrecer un catálogo de productos religiosos organizado en diversas categorías: sacramentales, artículos para sacramentos, rosarios, joyería, literatura católica y objetos litúrgicos y decorativos.

La API del sistema Sacré es un servicio REST desarrollado con **FastAPI**, diseñado para soportar la operación de la tienda virtual de artículos religiosos disponible inicialmente en Ecuador. Esta API proporciona los endpoints necesarios para gestionar el catálogo de productos, categorías, usuarios y procesos de compra, garantizando un acceso seguro, escalable y de alto rendimiento a la información del sistema.

## 🔹 2. Arquitectura del Proyecto

Este proyecto está organizado bajo los principios de una **Arquitectura Hexagonal Flexible**, combinada con una organización modular por dominios de negocio. El objetivo es mantener una clara separación de responsabilidades, alta cohesión y testeabilidad, sin incurrir en sobreingeniería innecesaria.

### 2.1. Filosofía: Arquitectura Hexagonal Flexible

En una arquitectura hexagonal estricta o purista, el núcleo de dominio debe ser 100% agnóstico a cualquier biblioteca externa, base de datos o framework web. En este proyecto se adoptó un enfoque **flexible y pragmático** fundamentado en las siguientes decisiones deliberadas:

1. **Acoplamiento intencional al framework (FastAPI & Pydantic)**:
   - **No se aísla FastAPI**: No existe intención de cambiar de framework web. Por ende, los servicios y la lógica de aplicación pueden utilizar utilidades de FastAPI o lanzar excepciones como `RequestValidationError` cuando se detectan violaciones de unicidad o de reglas de negocio. Esto permite que el sistema centralizado de manejo de errores de FastAPI traduzca dichas validaciones directamente en respuestas estandarizadas HTTP 400 Bad Request.
   - **Pydantic v2 en todas las capas**: Se utiliza como el estándar único de validación sintáctica, definición de contratos (DTOs) y generación de esquemas OpenAPI enriquecidos.
2. **Modelos ORM como Entidades de Dominio (SQLAlchemy)**:
   - Los modelos ubicados en `models/` son tanto los modelos de persistencia como las entidades de negocio.
   - Incorporan métodos del dominio y restricciones a nivel de base de datos, eliminando la necesidad de duplicar clases POPO (Plain Old Python Objects) y crear conversores (*mappers*) bidireccionales adicionales.
3. **Inversión de Dependencias estricta en Persistencia**:
   - A pesar de la flexibilidad con el framework, la capa de persistencia sí respeta la regla de inversión de dependencias: los servicios interactúan exclusivamente con **interfaces abstractas** de repositorios (`interfaces.py`), desacoplándose de las consultas SQL concretas y facilitando pruebas unitarias mediante dobles de prueba (*mocks*).

---

### 2.2. Estructura del Proyecto

```txt
.
├── .dockerignore                       # Exclusiones de archivos para la construcción de imágenes Docker
├── Dockerfile                          # Multi-stage Dockerfile para despliegues
├── pyproject.toml                      # Gestión de dependencias y configuración de herramientas
├── alembic/                            # Migraciones de esquema y versiones de base de datos
│
└── src/
    ├── scripts/                        # Utilidades CLI de mantenimiento y setup inicial
    │   ├── configure_roles.py          # Sincronización de roles y permisos en base de datos
    │   ├── create_admin.py             # Creación de usuario administrador inicial
    │   ├── create_asymmetric_keys.py   # Generación de claves criptográficas Ed25519 para JWT
    │   └── load_countries.py           # Carga del catálogo de países y estructuras administrativas
    │
    └── api/
        ├── common/                     # Componentes y contratos transversales
        │   ├── constants.py            # Constantes y mensajes de error globales
        │   ├── exceptions.py           # Excepciones base de dominio y aplicación
        │   ├── response.py             # Modelo unificado de respuesta API (Response[T])
        │   ├── schema.py               # Generadores dinámicos de esquemas OpenAPI para errores
        │   ├── utils.py                # Mixins y utilidades transversales
        │   ├── email/                  # Servicio y dependencias de correo electrónico SMTP
        │   └── payment/                # Servicios y dependencias de pasarela de pagos
        │
        ├── settings/                   # Configuración central del sistema
        │   ├── database.py             # Conexión asíncrona, pool asyncpg y gestión transaccional
        │   ├── exception_handlers.py   # Manejadores globales de excepciones (HTTP 400, 401, 403, 404, 409, 500, 502, 503)
        │   ├── http_client.py          # Cliente HTTP asíncrono global (httpx) con pool de conexiones y timeouts
        │   ├── models.py               # Registro central de modelos ORM para migraciones Alembic
        │   ├── openapi.py              # Metadatos, etiquetas y configuración personalizada de Swagger UI / OpenAPI
        │   ├── parameters.py           # Variables de entorno tipadas con Pydantic Settings
        │   ├── serialization.py        # Serializador JSON personalizado optimizado con orjson
        │   └── templates.py            # Motor de plantillas Jinja2 para renderizado dinámico en módulos
        │
        ├── modules/                    # Módulos de negocio delimitados por dominio
        │   └── <nombre_del_modulo>/    # Estructura uniforme de cada módulo
        │       ├── constants.py        # Constantes, enums y textos de validación del módulo
        │       ├── dependencies.py     # Proveedores FastAPI Depends (Inyección de dependencias)
        │       ├── dto.py              # Contratos de entrada y salida (Pydantic DTOs)
        │       ├── fixtures/           # (Opcional) Datos semilla o catálogos estáticos en JSON
        │       ├── models/             # Entidades de dominio y modelos SQLAlchemy
        │       ├── repositories/       # Capa de persistencia (Patrón Repositorio)
        │       │   ├── interfaces.py   # Contratos/Puertos de salida (Clases abstractas ABC)
        │       │   └── <entidad>.py    # Implementación concreta con SQLAlchemy AsyncSession
        │       ├── routers/            # Adaptadores primarios HTTP (Controladores FastAPI)
        │       ├── services/           # Casos de uso y lógica de negocio
        │       └── templates/          # (Opcional) Plantillas HTML/Jinja2 específicas del módulo
        │
        ├── gunicorn.py            # Configuración de Gunicorn con UvicornWorker
        └── main.py                     # Punto de entrada de la API (Instancia FastAPI, lifespan y rutas)
```

### 2.3. Anatomía Interna de un Módulo (`src/api/modules/<modulo>/`)

Cada módulo funciona como un dominio autocontenido y sigue un patrón de diseño uniforme:

#### Entidades de Dominio (`models/`)
- Clases que heredan de `Base` de SQLAlchemy.
- Cada módulo define sus tablas en un esquema de PostgreSQL específico.
- Integran validaciones de integridad, claves primarias UUID autogeneradas, relaciones ORM y métodos de negocio propios de la entidad.

#### Puertos de Persistencia (`repositories/interfaces.py`)
- Interfaces abstractas definidas con `abc.ABC` y `@abstractmethod`.
- Establecen el **contrato de persistencia** que requiere el dominio.
- No dependen de detalles de implementación de base de datos ni de sintaxis SQL.

#### Adaptadores de Persistencia (`repositories/<entidad>.py`)
- Implementan las interfaces abstractas de persistencia utilizando SQLAlchemy asíncrono.
- Los repositorios llaman a `self.__db.flush()` cuando necesitan sincronizar IDs generados u operaciones intermedias, pero nunca ejecutan `commit()` ni `rollback()` directamente. El ciclo de vida de la transacción está delegado a la sesión HTTP en `get_db_session()`.
- Centralizan todas las consultas SQL.

#### Casos de Uso y Negocio (`services/`)
- Clases que encapsulan la lógica de negocio y las reglas del dominio.
- Reciben los repositorios a través de sus interfaces abstractas en el método `__init__`, nunca instancian repositorios de forma interna.
- Ejecutan validaciones de negocio previas y transforman los datos persistidos en DTOs de salida listos para enviar al cliente.

#### Inyección de Dependencias (`dependencies.py`)
- Define las funciones factoría para resolver dependencias a través del sistema `Depends` de FastAPI:
  - **Factorías de Repositorios**: Inyectan la sesión `AsyncSession` (desde `get_db_session`) y retornan la implementación concreta tipada contra la interfaz correspondiente.
  - **Factorías de Servicios**: Inyectan los repositorios requeridos a través de sus interfaces y proveen la instancia del servicio.
  - **Seguridad y Permisos**: Incluye dependencias de autenticación JWT (`JWTAuthentication`) y validadores de roles y permisos granulares (`UserPermissionChecker`).

#### Adaptadores Primarios HTTP (`routers/`)
- Controladores organizados en endpoints específicos.
- Su responsabilidad es estrictamente de orquestación y transporte HTTP:
  - Definen rutas, métodos HTTP y documentación OpenAPI.
  - Inyectan el servicio mediante `Annotated[Service, Depends(get_service)]`.
  - Reciben el DTO de entrada validado automáticamente por FastAPI.
  - Llaman al método del caso de uso y devuelven la respuesta encapsulada en la clase estándar `Response[T]`.

#### Objetos de Transferencia de Datos (`dto.py`)
- Modelos Pydantic v2 que establecen los contratos de datos que entran y salen de la API.
- Separados en esquemas de creación (`Create...DTO`), actualización parcial (`Update...DTO`) y lectura (`Read...DTO`, `PrivateRead...DTO`).
- Incluyen metadatos `json_schema_extra={"x-validation-errors": [...]}` para autodocumentar en OpenAPI los mensajes exactos de error que produce cada campo en caso de falla.

#### Datos Semilla y Fixtures (`fixtures/`) [Opcional]
- Directorio opcional presente en aquellos módulos que requieren precargar o disponer de información inicial estática o de referencia.
- Sirve como fuente desacoplada para scripts de mantenimiento y carga inicial (como `src/scripts/load_countries.py`) o tareas de sembrado de datos (*seeders*), evitando acoplar catálogos o estructuras masivas al código fuente.

#### Plantillas y Renderizado Dinámico (`templates/`) [Opcional]
- Directorio opcional en aquellos módulos que requieren generar contenido HTML o texto dinámico asociado a sus flujos de negocio.
- Permite que cada módulo mantenga sus recursos visuales y de presentación co-localizados dentro de su propio dominio, siendo descubiertos automáticamente por el cargador centralizado de Jinja2 (`src/api/settings/templates.py`).

## 🔹 3. Tecnologías

<div>
    <img src="/assets/TechnologiesBackend.webp">
</div>

## 🔹 4. Instalación

> [!IMPORTANT]
> Necesitas tener instalado [Python 3.14](https://www.python.org/downloads/), [Poetry](https://python-poetry.org/docs/#installation) y [PostgreSQL](https://www.postgresql.org/download/) en tu sistema operativo.

### Paso 1: Clonar el repositorio

```txt
git clone git@github.com:viavervit-dev/api-sacre.git
cd api-sacre
```

### Paso 2: Configurar variables de entorno

Crea un archivo `.env` dentro de la carpeta `src` del proyecto tomando como plantilla la siguiente estructura:

```env
# === Aplicación ===
DEBUG=true
ENABLE_DOCS=true
CORS_ORIGINS="http://localhost:3000,http://127.0.0.1:3000"
ADMIN_EMAIL=<value>
ADMIN_PASSWORD=<value>
ADMIN_FIRST_NAMES=<value>
ADMIN_LAST_NAMES=<value>


# === Base de Datos ===
ALEMBIC_DATABASE_URL="postgresql+psycopg2://api_user:api_password@localhost:5432/fastapi_db"
DATABASE_URL="postgresql+asyncpg://api_user:api_password@localhost:5432/fastapi_db"
DB_STATEMENT_TIMEOUT=10000
DB_POOL_MAX_OVERFLOW=5
DB_COMMAND_TIMEOUT=15
DB_POOL_RECYCLE=1800
DB_POOL_TIMEOUT=5
DB_POOL_SIZE=10
DB_ECHO=false
DB_JIT=off


# === Seguridad y Autenticación ===
PRIVATE_KEY=<value>
PUBLIC_KEY=<value>


# === Gestor de Pagos ===
API_PAYMENT_LINKS=<value>
API_PAYMENT_STORE_ID=<value>
API_PAYMENT_KEY=<value>


# === Correo Electrónico (SMTP) ===
MAIL_USERNAME=<value>
MAIL_PASSWORD=<value>
MAIL_FROM_ADDRESS=<value>
MAIL_SERVER=<value>
MAIL_PORT=465
MAIL_USE_SSL=true
MAIL_STARTTLS=false
MAIL_TIMEOUT=15


# === Servidor ===
HOST="127.0.0.1"
PORT=8080
WORKERS=4
FORWARDED_ALLOW_IPS="*"
```

> [!IMPORTANT]
> **Valores esenciales que debes configurar antes de continuar:**
> - **Entorno y Seguridad (`ENABLE_DOCS`, `CORS_ORIGINS`, `FORWARDED_ALLOW_IPS`)**:
>   - `ENABLE_DOCS`: Habilita o restringe la exposición pública de `/docs`, `/redoc` y `/openapi.json`. Si no se define, se sincroniza con `DEBUG` (activo en desarrollo, desactivado en producción).
>   - `CORS_ORIGINS`: Lista de orígenes web autorizados separados por coma (ej. `"https://sacre.ec,https://admin.sacre.ec"` o `http://localhost:3000` en desarrollo). Fundamental para que los navegadores admitan el envío de cookies de autenticación `HttpOnly`.
>   - `FORWARDED_ALLOW_IPS`: Direcciones IP de proxies inversos o balanceadores (Cloudflare, Nginx, ALB) desde los cuales se confía en las cabeceras `X-Forwarded-*`. En Docker o redes internas privadas se usa `"*"` para registrar la IP real del cliente.
> - **Datos del Administrador (`ADMIN_*`)**: Reemplaza los marcadores `<value>` por el correo electrónico, contraseña segura, nombres y apellidos del administrador inicial. Estos datos serán utilizados posteriormente por el script `src.scripts.create_admin` para registrar el usuario en la base de datos (ver **Paso 8**).
> - **Credenciales de Base de Datos**: Asegúrate de que el usuario (`api_user`), la contraseña (`api_password`) y el nombre de la base de datos (`fastapi_db`) en `DATABASE_URL` y `ALEMBIC_DATABASE_URL` coincidan exactamente con los que configures en el **Paso 3**. Nota que `ALEMBIC_DATABASE_URL` utiliza el driver síncrono `postgresql+psycopg2://` para migraciones, mientras que `DATABASE_URL` utiliza el driver asíncrono `postgresql+asyncpg://` para la API.
> - **Claves Asimétricas (`PRIVATE_KEY` y `PUBLIC_KEY`)**: Requieren un par de claves criptográficas asimétricas Ed25519 en formato PEM. Se generarán ejecutando el script del proyecto tras instalar las dependencias (ver **Paso 5**).
> - **Gestor de Pagos y Correo SMTP**: Si estás en un entorno de desarrollo local y vas a probar flujos de checkout, compra o notificaciones, ingresa las credenciales provistas por la pasarela en `API_PAYMENT_*` y una contraseña de aplicación en `MAIL_*`.


### Paso 3: Crear base de datos local

Este proyecto utiliza **PostgreSQL** como motor de base de datos. Para la conexión se emplea SQLAlchemy de forma asíncrona (`asyncpg`) para el rendimiento de la API, y `psycopg2` como driver síncrono para la gestión de migraciones con Alembic. Asegúrate de tener el servicio de PostgreSQL corriendo. Si estás usando WSL o Linux, abre tu terminal y sigue estos pasos:

1. Accede a la consola de PostgreSQL usando el usuario administrador:
   ```txt
   sudo -u postgres psql
   ```

2. Ejecuta los siguientes comandos SQL para crear el usuario, la base de datos y otorgar los permisos (cambia `api_user`, `api_password` y `fastapi_db` por los nombres que prefieras y tambien en `src/.env`):
   ```txt
   -- 1. Crear el usuario con su contraseña
   CREATE USER api_user WITH PASSWORD 'api_password';

   -- 2. Crear la base de datos
   CREATE DATABASE fastapi_db;

   -- 3. Otorgar todos los privilegios sobre la base de datos al usuario
   GRANT ALL PRIVILEGES ON DATABASE fastapi_db TO api_user;

   -- 4. Otorgar permisos sobre el esquema public (Necesario en PostgreSQL 15+)
   \c fastapi_db
   GRANT ALL ON SCHEMA public TO api_user;

   -- Salir de la consola
   \q
   ```

### Paso 4: Instalar dependencias

Este comando instalará todas las dependencias del proyecto.

```txt
poetry env use python3.14
poetry install
```

### Paso 5: Generar claves asimétricas para JWT

El sistema utiliza firmas criptográficas asimétricas (algoritmo Ed25519) para la emisión y verificación de tokens JWT. Para generar el par de claves, ejecuta el siguiente comando:

```txt
python3.14 -m src.scripts.create_asymmetric_keys
```

El script imprimirá por consola la **clave privada** y la **clave pública** en formato PEM. Copia cada bloque de texto y pégalo entre comillas en tu archivo `src/.env` dentro de las variables `PRIVATE_KEY` y `PUBLIC_KEY` respectivamente:

```txt
PRIVATE_KEY="-----BEGIN PRIVATE KEY-----
...
-----END PRIVATE KEY-----"

PUBLIC_KEY="-----BEGIN PUBLIC KEY-----
...
-----END PUBLIC KEY-----"
```

### Paso 6: Instalar hooks

Estos comandos instalarán los hooks de [pre-commit](https://pre-commit.com/) configurados en el proyecto para validación de código y mensajes de commit.

```txt
pre-commit install
pre-commit install --hook-type commit-msg
```

### Paso 7: Aplicar migraciones

Aplica las migraciones con Alembic para generar las tablas y esquemas en PostgreSQL:

```txt
alembic upgrade head
```

### Paso 8: Ejecutar scripts de inicialización

Ejecuta los scripts necesarios para configurar roles y permisos, cargar el catálogo de países y registrar al usuario administrador inicial:

```txt
# 1. Configurar roles y permisos
python3.14 -m src.scripts.configure_roles

# 2. Cargar catálogo de países y organización territorial
python3.14 -m src.scripts.load_countries

# 3. Crear usuario administrador
python3.14 -m src.scripts.create_admin
```

### Paso 9: Iniciar servidor de desarrollo

Este comando iniciará el servidor utilizando el `HOST` y `PORT` definidos en el archivo `src/.env`. Si `DEBUG=true`, la recarga automática estará habilitada.

```txt
python3.14 -m src.api.main
```

## 🔹 5. Base de Datos y Migraciones

Este proyecto usa **Alembic** para gestionar las migraciones del esquema de base de datos. Los modelos ORM se definen en la carpeta `models/` de cada módulo y deben registrarse en `src/api/settings/models.py` para que Alembic los detecte.

### Flujo de trabajo

Cada vez que crees o modifiques un modelo ORM, sigue estos pasos:

**1. Crear o modificar el modelo** en `src/api/modules/<modulo>/models/<modelo>.py`

**2. Registrar el modelo** en `src/api/settings/models.py` (solo si es un modelo nuevo):

```python
# api/settings/models.py
from src.api.modules.customers.models.customer import Customer
from src.api.modules.products.models.product import Product
```

**3. Generar la migración** (Alembic compara el modelo con el estado actual de la BD):

```txt
alembic revision --autogenerate -m "descripcion_del_cambio"
```

**4. Aplicar la migración** a la base de datos:

```txt
alembic upgrade head
```

### Otros comandos útiles

| Comando | Descripción |
|---------|-------------|
| `alembic upgrade head` | Aplica todas las migraciones pendientes |
| `alembic downgrade -1` | Revierte la última migración aplicada |
| `alembic downgrade base` | Revierte todas las migraciones (esquema vacío) |
| `alembic current` | Muestra la revisión actualmente aplicada en la BD |
| `alembic history` | Lista todas las migraciones en orden cronológico |


## 🔹 6. Scripts Disponibles

El proyecto incluye scripts de mantenimiento y configuración inicial dentro del directorio `src/scripts/`. Estos scripts interactúan directamente con la base de datos.

### Configuración de Roles y Permisos

Para inicializar o actualizar los permisos y roles de los usuarios en la base de datos, ejecuta el siguiente comando en la raíz del proyecto:

```txt
python3.14 -m src.scripts.configure_roles
```

**¿Qué hace este script?**
- Crea los permisos basados en los modelos existentes.
- Crea los grupos o roles predeterminados.
- Asocia automáticamente los permisos correctos a cada grupo.
- Limpia los permisos obsoletos de los grupos si estos fueron removidos de la configuración.

*(Si necesitas agregar nuevos roles o ajustar los permisos de un grupo existente, debes modificar los diccionarios `GROUPS` y `PERMISSIONS` dentro de `src/scripts/configure_roles.py` antes de correr el comando).*

### Carga de Países

Para inicializar o actualizar el catálogo de países y sus estructuras territoriales en la base de datos, ejecuta el siguiente comando en la raíz del proyecto:

```txt
python3.14 -m src.scripts.load_countries
```

**¿Qué hace este script?**
- Lee los archivos de fixtures en formato JSON ubicados en `src/api/modules/countries/fixtures/`.
- Extrae el nombre y código del país a partir del nombre de cada archivo, validando que cumpla con el formato `<Nombre>_<CODIGO>.json` (por ejemplo, `Ecuador_EC.json`).
- Consulta la tabla `countries.country` para verificar si el país ya existe por código o por nombre.
- Si el país existe, actualiza su nombre, código y estructura administrativa (`administrative_structure`).
- Si el país no existe, crea un nuevo registro con la información y la estructura territorial proporcionada.

*(Si deseas registrar un nuevo país o modificar su organización territorial, añade o actualiza el archivo JSON correspondiente en `src/api/modules/countries/fixtures/` asegurándote de seguir el formato de nombre `<Nombre>_<CODIGO>.json` antes de ejecutar el comando).*

### Creación de Administrador

Para crear un usuario administrador inicial en la base de datos, ejecuta el siguiente comando en la raíz del proyecto:

```txt
python3.14 -m src.scripts.create_admin
```

**¿Qué hace este script?**
- Verifica si el usuario ya existe para evitar duplicados.
- Verifica si existe el grupo de permisos de administrador.
- Crea el usuario con el rol de administrador y configura su contraseña.
- Asigna el usuario al grupo de permisos correspondiente.
- Crea el perfil del administrador en la base de datos.

*(Antes de ejecutar el comando, asegúrate de tener configuradas las siguientes variables de entorno en tu archivo `.env`: `ADMIN_EMAIL`, `ADMIN_PASSWORD`, `ADMIN_FIRST_NAMES` y `ADMIN_LAST_NAMES`).*

### Generación de Claves Asimétricas

Para generar las claves asimétricas (Ed25519) necesarias para la autenticación JWT, ejecuta el siguiente comando en la raíz del proyecto:

```txt
python3.14 -m src.scripts.create_asymmetric_keys
```

**¿Qué hace este script?**
- Genera un nuevo par de claves criptográficas asimétricas (privada y pública) utilizando el algoritmo Ed25519.
- Imprime las claves generadas en la consola en formato PEM listas para ser copiadas.

*(Debes copiar los bloques de texto generados y pegarlos en tu archivo `.env` bajo las variables `PRIVATE_KEY` y `PUBLIC_KEY` respectivamente).*

## 🔹 7. Contribución

Consulta nuestra guía [CONTRIBUTING](CONTRIBUTING.md) para conocer las reglas y buenas prácticas que debes seguir antes de contribuir al proyecto. Este documento proporciona instrucciones detalladas sobre cómo configurar tu entorno de desarrollo, trabajar correctamente en el repositorio, proponer cambios de manera efectiva y seguir el estilo de código adoptado por el equipo.

## 🔹 8. Colaboradores

A continuación se presentan a las personas que están aportando al desarrollo de este proyecto.

| Nombre | Enlaces | Roles |
|--------|:-------:|:-----:|
| Carlos Andres Aguirre Ariza | [GitHub](https://github.com/The-Asintota) - [LinkedIn](https://www.linkedin.com/in/carlosaguirredev/) | Backend, Documentación, DevOps |