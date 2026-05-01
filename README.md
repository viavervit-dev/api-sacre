<div>
    <img src="/assets/ProjectBanner.webp">
</div>

## 🔹 1. API Sacré

El sistema Sacré será una tienda virtual disponible inicialmente en **Ecuador**. Su propósito es ofrecer un catálogo de productos religiosos organizado en diversas categorías: sacramentales, artículos para sacramentos, rosarios, joyería, literatura católica y objetos litúrgicos y decorativos.

La API del sistema Sacré es un servicio REST desarrollado con **FastAPI**, diseñado para soportar la operación de la tienda virtual de artículos religiosos disponible inicialmente en Ecuador. Esta API proporciona los endpoints necesarios para gestionar el catálogo de productos, categorías, usuarios y procesos de compra, garantizando un acceso seguro, escalable y de alto rendimiento a la información del sistema.

## 🔹 2. Arquitectura del Proyecto

Este proyecto está organizado siguiendo una arquitectura modular y escalable, facilitando el mantenimiento y la reutilización de código.

### 📁 Estructura de Carpetas

```txt
api-sacre/
├── alembic/                        # Configuración y scripts de migraciones (Alembic)
│   ├── versions/                   # Archivos de migración generados automáticamente
│   └── env.py                      # Entorno de ejecución de migraciones
├── src/                            # Código fuente de la aplicación
│   ├── common/                     # Utilidades y contratos compartidos
│   │   ├── constants.py            # Constantes globales
│   │   ├── response.py             # Modelo genérico de respuesta estándar
│   │   └── schema.py               # Esquemas base de Pydantic
│   ├── config/                     # Configuración central de la aplicación
│   │   ├── database.py             # Conexión a base de datos y pool
│   │   ├── exception_handlers.py   # Manejadores de excepciones globales
│   │   ├── models.py               # Registro de modelos para Alembic
│   │   ├── parameters.py           # Variables de entorno
│   │   └── serialization.py        # Configuración de serialización JSON
│   ├── modules/                    # Módulos de negocio (separados por dominio)
│   │   └── <nombre_del_modulo>/    # Estructura genérica de un módulo
│   │       ├── dto.py              # Esquemas de transferencia de datos (Pydantic)
│   │       ├── models/             # Entidades ORM del dominio
│   │       ├── repositories/       # Acceso a base de datos (Patrón Repository)
│   │       ├── routers/            # Endpoints y rutas de FastAPI
│   │       └── services/           # Lógica de negocio (Casos de uso)
│   ├── scripts/                    # Scripts de configuración y mantenimiento
│   │   └── configure_roles.py      # Inicialización de roles y permisos
│   └── main.py                     # Punto de entrada: instancia FastAPI, lifespan y rutas base
├── workflow/                       # Guías y convenciones del equipo
│   ├── branching_strategy.md       # Estrategia de ramas Git
│   ├── create_branch.md            # Proceso para crear nuevas ramas
│   └── create_commit.md            # Convenciones de mensajes de commit
```

## 🔹 3. Tecnologías

<div>
    <img src="/assets/TechnologiesBackend.webp">
</div>

## 🔹 4. Instalación

> [!IMPORTANT]
> Necesitas tener instalado [Python 3.12](https://www.python.org/downloads/) y [Poetry](https://python-poetry.org/docs/#installation)

### Paso 1: Clonar el repositorio

```txt
git clone git@github.com:viavervit-dev/api-sacre.git
cd api-sacre
```

### Paso 2: Configurar variables de entorno

Crea un archivo `.env` en la raíz del proyecto con las siguientes variables:

```txt
# === Aplicación ===
APP_NAME="API Sacre"
DEBUG=true

# === Base de Datos ===
# Desarrollo local (SQLite, no requiere servidor)
DATABASE_URL="sqlite+aiosqlite:///./sacre.db"

# Producción (PostgreSQL)
# DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/api_sacre"
DB_POOL_MAX_OVERFLOW=10
DB_POOL_SIZE=10

# === Seguridad ===
SECRET_KEY="your-super-secret-key-min-32-chars"

# === Servidor ===
HOST="127.0.0.1"
PORT=8080
WORKERS=4
```

> [!IMPORTANT]
> Reemplaza los valores de `DATABASE_URL` y `SECRET_KEY` con tus credenciales reales. Nunca subas el archivo `.env` al repositorio.

> [!TIP]
> Para generar una `SECRET_KEY` segura, ejecuta el siguiente comando:
>
> ```bash
> python -c "import secrets; print(secrets.token_urlsafe(64))"
> ```

### Paso 3: Instalar hooks

Estos comandos instalarán los hooks de [pre-commit](https://pre-commit.com/) configurados en el proyecto para validación de código y mensajes de commit.

```txt
pre-commit install
pre-commit install --hook-type commit-msg
```

### Paso 4: Instalar dependencias

Este comando instalará todas las dependencias del proyecto.

```txt
poetry install
```

### Paso 5: Iniciar servidor de desarrollo

Este comando iniciará el servidor utilizando el `HOST` y `PORT` definidos en el archivo `.env`. Si `DEBUG=true`, la recarga automática estará habilitada.

```txt
python -m src.main
```

## 🔹 5. Base de Datos y Migraciones

Este proyecto usa **Alembic** para gestionar las migraciones del esquema de base de datos. Los modelos ORM se definen en la carpeta `models/` de cada módulo y deben registrarse en `src/config/models.py` para que Alembic los detecte.

### Flujo de trabajo

Cada vez que crees o modifiques un modelo ORM, sigue estos pasos:

**1. Crear o modificar el modelo** en `src/modules/<modulo>/models/<modelo>.py`

**2. Registrar el modelo** en `src/config/models.py` (solo si es un modelo nuevo):

```python
# src/config/models.py
from src.modules.customers.models.customer import Customer
from src.modules.products.models.product import Product
```

> [!NOTE]
> Alembic no descubre los modelos automáticamente. `src/config/models.py` es el registro central que le indica a Alembic qué tablas existen. `alembic/env.py` importa este archivo y nunca necesita modificarse al agregar nuevos modelos.

**3. Generar la migración** (Alembic compara el modelo con el estado actual de la BD):

```bash
alembic revision --autogenerate -m "descripcion_del_cambio"
```

> [!IMPORTANT]
> Revisa siempre el archivo generado en `alembic/versions/` antes de aplicarlo. El `autogenerate` detecta la mayoría de cambios, pero no todos (p. ej. cambios en `CHECK` constraints, lógica de columnas calculadas).

**4. Aplicar la migración** a la base de datos:

```bash
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

```bash
python -m src.scripts.configure_roles
```

**¿Qué hace este script?**
- Crea los permisos basados en los modelos existentes.
- Crea los grupos o roles predeterminados.
- Asocia automáticamente los permisos correctos a cada grupo.
- Limpia los permisos obsoletos de los grupos si estos fueron removidos de la configuración.

*(Si necesitas agregar nuevos roles o ajustar los permisos de un grupo existente, debes modificar los diccionarios `GROUPS` y `PERMISSIONS` dentro de `src/scripts/configure_roles.py` antes de correr el comando).*

## 🔹 7. Contribución

Consulta nuestra guía [CONTRIBUTING](CONTRIBUTING.md) para conocer las reglas y buenas prácticas que debes seguir antes de contribuir al proyecto. Este documento proporciona instrucciones detalladas sobre cómo configurar tu entorno de desarrollo, trabajar correctamente en el repositorio, proponer cambios de manera efectiva y seguir el estilo de código adoptado por el equipo.

## 🔹 8. Colaboradores

A continuación se presentan a las personas que están aportando al desarrollo de este proyecto.

| Nombre | Enlaces | Roles |
|--------|:-------:|:-----:|
| Carlos Andres Aguirre Ariza | [GitHub](https://github.com/The-Asintota) - [LinkedIn](https://www.linkedin.com/in/carlosaguirredev/) | Backend, Documentación, DevOps |