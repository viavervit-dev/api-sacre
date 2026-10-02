from typing import Any

API_DESCRIPTION = """
API Sacré es el servicio backend central que impulsa la tienda virtual de artículos
religiosos católicos (sacramentales, rosarios, joyería, literatura católica, artículos
litúrgicos y para sacramentos), diseñada inicialmente para operar en Ecuador con
proyección de expansión regional.

### Propósito y Alcance

Al encontrarse en fase activa de desarrollo, la API centraliza la base operativa y
administrativa del negocio:

- Catálogo e inventario.
- Gestión de usuarios.
- Acceso y Seguridad.
- Flujo de Compra y Checkout.
- Pagos y Facturación.
- Logística y Despachos.

---

### Estructura de Respuesta Estándar
Todos los endpoints devuelven un formato unificado basado en `Response[T]`:
```json
{
  "success": true,
  "pagination": false,
  "message": "Mensaje descriptivo del resultado.",
  "data": { ... }
}
```

Para consultas paginadas, la propiedad `data` adopta la siguiente estructura:
```json
{
  "items": [ ... ],
  "meta": {
    "total": 120,
    "offset": 0,
    "limit": 50
  }
}
```

---

### Seguridad y Autenticación
La plataforma cuenta con una arquitectura preparada para admitir múltiples métodos de
autenticación.

#### Métodos de Autenticación:
1. **JSON Web Tokens (JWT)** `[Disponible]`:
   - **Firma Criptográfica:** Asimétrica con algoritmo **EdDSA (Ed25519)**.
   - **Ciclo de Vida:**
     - `Access Token`: Caducidad corta (**15 minutos**).
     - `Refresh Token`: Caducidad extendida (**4 días**).

#### Control de Acceso:
- **Modelo:** Control de acceso basado en roles (**RBAC**) con validación de permisos
  granulares por recurso y operación.
"""

OPENAPI_TAGS: list[dict[str, Any]] = [
    {
        "name": "Autenticación",
        "description": ("Operaciones de autenticación y control de sesiones."),
    },
    {
        "name": "Usuarios",
        "description": ("Administración y registro de los diferentes usuarios."),
    },
    {
        "name": "Inventario",
        "description": ("Gestión del catálogo comercial."),
    },
    {
        "name": "Países",
        "description": "Consulta de datos geográficos y parametrización regional del sistema.",
    },
    {
        "name": "Utilidades",
        "description": (
            "Monitoreo del sistema, sondas de disponibilidad y verificación de componentes."
        ),
    },
]

SWAGGER_UI_PARAMETERS: dict[str, Any] = {
    "filter": True,
    "persistAuthorization": True,
    "displayRequestDuration": True,
    "defaultModelsExpandDepth": -1,
}
