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
├── src/                            # Código fuente de la aplicación
│   ├── common/                     # Utilidades y contratos compartidos
│   │   └── response.py             # Modelo genérico de respuesta estándar `Response[T]`
│   ├── config/                     # Configuración central de la aplicación
│   │   ├── database.py             # Pool de conexiones asíncrono a la base de datos
│   │   ├── exception_handlers.py   # Manejadores globales de excepciones HTTP y de validación
│   │   ├── parameters.py           # Variables de entorno y parámetros de la aplicación
│   │   └── serialization.py        # Respuesta JSON de alto rendimiento con orjson
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
DATABASE_URL="postgresql+asyncpg://user:password@localhost:5432/api_sacre"
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

## 🔹 5. Contribución

Consulta nuestra guía [CONTRIBUTING](CONTRIBUTING.md) para conocer las reglas y buenas prácticas que debes seguir antes de contribuir al proyecto. Este documento proporciona instrucciones detalladas sobre cómo configurar tu entorno de desarrollo, trabajar correctamente en el repositorio, proponer cambios de manera efectiva y seguir el estilo de código adoptado por el equipo.

## 🔹 6. Colaboradores

A continuación se presentan a las personas que están aportando al desarrollo de este proyecto.

| Nombre | Enlaces | Roles |
|--------|:-------:|:-----:|
| Carlos Andres Aguirre Ariza | [GitHub](https://github.com/The-Asintota) - [LinkedIn](https://www.linkedin.com/in/carlosaguirredev/) | Backend, Documentación, DevOps |