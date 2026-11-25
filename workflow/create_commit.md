# 🔹 Guía de Creación de Commits

El uso de [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) permite mantener un historial de cambios claro, consistente y fácil de entender en cualquier entorno de trabajo colaborativo. Conventional Commits no solo define un formato de mensajes, sino que funciona como una guía de comunicación técnica que facilita el trabajo en equipo en cualquier tipo de proyecto.

## 🔹 1. Beneficios

Adoptar esta convención aporta varios beneficios:

- 📖 **Claridad:** Cada commit deja explícito si se trata de una nueva funcionalidad, una corrección, un cambio en la documentación, una tarea de mantenimiento, entre otros.
- 🤝 **Colaboración:** Al utilizar un mismo lenguaje y formato, todas las personas que contribuyen entienden rápidamente la naturaleza de cada cambio.
- ⚙️ **Automatización:** Muchas herramientas pueden generar automáticamente changelogs, manejar versionado semántico ([semver](https://semver.org/lang/es/)) y crear notas de lanzamiento a partir de los commits.
- 🔍 **Trazabilidad:** Resulta más sencillo identificar cuándo y dónde se introdujo una funcionalidad, una mejora de rendimiento o la corrección de un error.
- 🚀 **Escalabilidad:** Cuanto mayor es el número de personas involucradas, más útil resulta contar con un estándar común que evite confusiones y mantenga ordenado el flujo de trabajo.


## 🔹 2. Estructura del Commit

La estructura de un commit sigue el siguiente formato:

```txt
<tipo>(<scope>): <descripción>

<opcional cuerpo>

<opcional notas al pie>
```

| Elemento | Descripción |
|----------|-------------|
| `<tipo>` | Indica la naturaleza del cambio realizado. |
| `<scope>` | (opcional) Señala el ámbito o área afectada por el cambio. |
| `<descripción>` | Frase nominal que describe el cambio. Máximo 72 caracteres. |
| `<cuerpo>` | Texto descriptivo con el contexto, propósito e impacto del cambio. No usar solo listas ni tecnicismos/clases internas. |
| `<notas de pie>` | Información especial como referencias a incidencias, tickets o cambios que rompen compatibilidad (BREAKING CHANGE). |

## 🔹 3. Estilo de Redacción

### 3.1. ¿Por qué frases nominales?

Este proyecto utiliza [semantic-release](https://semantic-release.gitbook.io/semantic-release) para automatizar la publicación de releases. Los mensajes de commit se extraen directamente para generar las notas de la release. Por eso, la forma en que escribimos los commits afecta directamente cómo se leen las notas públicas del proyecto.

> [!IMPORTANT]
> Los mensajes de commit deben escribirse como **frases nominales descriptivas**, no como comandos imperativos. Esto garantiza que las release notes sean profesionales y legibles.

### 3.2. El Problema con el Imperativo

El estándar original de Conventional Commits sugiere usar modo imperativo ("Agregar", "Corregir", "Implementar"). Sin embargo, esto genera release notes que parecen una lista de órdenes:

```markdown
## Funcionalidades
- Agregar botón de login
- Implementar autenticación OAuth
- Crear endpoint de productos
```

Al usar **frases nominales** (sustantivos y descripciones), las release notes se leen de forma fluida y profesional:

```markdown
## Funcionalidades
- botón de login con opciones de redes sociales
- autenticación con Google OAuth
- endpoint de creación de productos (`POST /products`)

## Correcciones
- corrección de overflow en tarjetas móviles
- manejo de expiración de tokens JWT
```

| ❌ Imperativo (NO usar) | ✅ Frase Nominal (usar) |
|------------------------|------------------------|
| `Agregar login con Google` | `login con Google OAuth` |
| `Corregir overflow en cards` | `corrección de overflow en tarjetas móviles` |
| `Implementar lazy loading` | `carga diferida para imágenes de productos` |
| `Crear endpoint de productos` | `endpoint de creación de productos` |
| `Actualizar dependencias` | `actualización de dependencias de seguridad` |
| `Eliminar código deprecado` | `limpieza de código deprecado` |
| `Refactorizar servicio de usuario` | `refactorización del servicio de usuario` |

### 3.3. Redacción del Cuerpo (`<cuerpo>`)

Cuando el cambio requiera contexto adicional o justificación funcional (especialmente en squash merges hacia `development`), se debe incluir un cuerpo explicativo separado del asunto por una línea en blanco.

> [!IMPORTANT]
> El cuerpo del commit debe iniciar con un **texto descriptivo continuo** (uno o dos párrafos breves) que explique el **propósito, impacto y alcance** de la modificación sin detallar nombres de clases internas, métodos privados o tecnicismos de bajo nivel del código. Cuando sí corresponda mencionar conceptos relacionados con el código (librerías, funciones, clases, rutas de ficheros, directorios o endpoints), envuélvelos entre backticks (`` ` ``).
>
> Si resulta útil para estructurar o presentar puntos clave, componentes o pasos, es totalmente válido incluir una **lista con viñetas (`- ...`)** o una **enumeración (`1. ...`)**, siempre que se coloque **justo después del párrafo de contexto**.

| ❌ A evitar en el cuerpo | ✅ Recomendado en el cuerpo |
|--------------------------|----------------------------|
| Solo listas de viñetas o ítems sueltos sin párrafo introductorio | Párrafo narrativo estructurado inicial, seguido opcionalmente de una lista o numeración si aporta claridad |
| Nombres de clases internas, funciones o métodos (`UploadFileService`, `CadFileRepository`, `process_file()`) | Capacidades funcionales o de dominio ("servicio de procesamiento", "persistencia en base de datos") |
| Explicaciones hiper-técnicas de bajo nivel | Explicaciones claras sobre el valor aportado, la robustez, el rendimiento o la seguridad |

### 3.5. Reglas de Redacción

| Regla | Descripción |
|-------|-------------|
| **Inicio en minúscula** | La descripción debe iniciar siempre en minúscula, salvo que empiece con una sigla/concepto técnico (ej. `DTO`, `API`, `JWT`) o el nombre propio de una clase/módulo entre backticks (ej. `` `CustomerRepository` ``, `` `UploadFileService` ``). |
| **Backticks para código** | Envuelve entre backticks (`` ` ``) los conceptos relacionados con el código: librerías, funciones, clases, rutas de ficheros, directorios o endpoints (ej. `` `CustomerService` ``, `` `src/api/settings/` ``, `` `POST /products` ``). |
| **Sin verbos al inicio** | No empieces con "Agregar", "Corregir", "Crear", etc. |
| **Usa sustantivos** | Describe QUÉ es el cambio, no qué hacer. |
| **Máximo 72 caracteres** | Mantén la descripción concisa (considerando los caracteres de los backticks). |
| **Sin punto final** | No termines con punto. |

> [!NOTE]
> Al ejecutar `git commit -m` en terminal (`bash`/`zsh`), usa **comillas simples** (`'...'`) o el editor (`git commit`) para evitar que la shell interprete los backticks (`` ` ``) como ejecución de comandos.

## 🔹 4. Prefijos Reservados

Este proyecto utiliza **squash merge** para integrar Pull Requests hacia `development`. Esto significa que todos los commits de una rama se combinan en un único commit al fusionar.

> [!IMPORTANT]
> Los prefijos `feat`, `fix` y `perf` están **reservados** para el commit final del squash merge, ya que impactan directamente el versionado semántico.

Imagina que estás creando un nuevo endpoint `POST /products`:

```txt
# Durante el desarrollo (en tu feature branch)
add(products): modelo `Product` con campos base
add(products): `ProductRepository` con métodos CRUD
add(products): `CreateProductService`
add(products): endpoint POST en `ProductController`
add(products): middleware de validación de entrada
test(products): tests unitarios y de integración

# Al hacer squash merge (mensaje final del PR)
feat(api): endpoint de creación de productos (`POST /products`)
```

## 🔹 5. Tipos de Commit

Los tipos clasifican los cambios de manera uniforme y permiten que cualquier persona del equipo entienda rápidamente la intención del commit sin tener que revisar el código.

### 5.1. `feat` - Nueva Funcionalidad ⚡

> [!NOTE]
> Este prefijo está **reservado para squash merge**.

**Qué es:** Funcionalidad completa visible para el usuario/cliente, lista para producción.

**✅ Cuándo usarlo:**
- Como mensaje final del squash merge cuando la PR agrega una nueva capacidad.
- La funcionalidad está completa, probada y lista para usuarios.

**❌ Cuándo NO usarlo:**
- En commits intermedios durante el desarrollo (usa `add`).
- Para cambios parciales o trabajo en progreso.

**Ejemplos (mensaje de squash merge):**
```txt
# Backend
feat(usuarios): endpoint de creación de clientes (`POST /customers`)
feat(facturación): generación automática de facturas electrónicas
feat(autenticación): login con Google OAuth 2.0

# Frontend
feat(productos): componente de búsqueda con filtros avanzados
feat(carrito): vista previa del pedido antes de confirmar
feat(dashboard): gráficos interactivos de ventas mensuales

# Móvil / Desktop
feat(notificaciones): notificaciones push en tiempo real
feat(offline): modo sin conexión con sincronización automática
```

### 5.2. `fix` - Corrección de Bug ⚡

> [!NOTE]
> Este prefijo está **reservado para squash merge**.

**Qué es:** Corrección completa de un bug, incluyendo todos los cambios necesarios.

**✅ Cuándo usarlo:**
- Como mensaje final del squash merge cuando la PR corrige un bug.
- La corrección está completa y verificada.

**❌ Cuándo NO usarlo:**
- En commits intermedios durante el desarrollo (usa `add`).
- Para cambios meramente estéticos o refactorizaciones.

**Ejemplos (mensaje de squash merge):**
```txt
# Backend
fix(facturación): corrección de cálculo de IVA en productos exentos
fix(autenticación): manejo de tokens JWT expirados
fix(reportes): corrección de filtro de fechas en exportación

# Frontend
fix(formularios): validación de campos requeridos en registro
fix(tabla): paginación incorrecta al filtrar resultados
fix(modal): cierre inesperado al hacer clic fuera del área

# General
fix(api): respuesta 500 al enviar payload vacío
fix(permisos): acceso denegado a usuarios con rol administrador
```

### 5.3. `perf` - Mejora de Rendimiento ⚡

> [!NOTE]
> Este prefijo está **reservado para squash merge**.

**Qué es:** Optimización completa con impacto medible en rendimiento.

**✅ Cuándo usarlo:**
- Como mensaje final del squash merge cuando la PR mejora rendimiento.
- La optimización está completa y su impacto ha sido medido.

**❌ Cuándo NO usarlo:**
- En commits intermedios durante el desarrollo (usa `add`).
- Si el objetivo fue reorganizar código sin foco en rendimiento.

**Ejemplos (mensaje de squash merge):**
```txt
# Backend
perf(reportes): optimización de consulta de ventas (60% más rápido)
perf(api): paginación de resultados en endpoint `/products`
perf(cache): caché `Redis` para datos de catálogo

# Frontend
perf(imágenes): carga diferida (lazy loading) en galería
perf(bundle): división de código para carga inicial más rápida
perf(tabla): virtualización de filas en listados grandes

# Base de datos
perf(db): índices para búsquedas por fecha y cliente
perf(consultas): reducción de N+1 en listado de pedidos
```

### 5.4. `add` - Bloque de Construcción 🔨

**Qué es:** Commit intermedio que forma parte de una funcionalidad, corrección u optimización más grande.

**✅ Cuándo usarlo:**
- Agregas un modelo, servicio, repositorio o componente que será parte de una feature.
- Implementas una parte de la solución a un bug.
- Cualquier paso intermedio hacia un objetivo mayor.

**❌ Cuándo NO usarlo:**
- Para el commit final de squash merge (usa `feat`, `fix` o `perf`).
- Para cambios que son completos y autónomos.

**Ejemplos:**
```txt
# Backend
add(clientes): modelo `Customer` con validaciones
add(clientes): `CustomerRepository` con métodos CRUD
add(api): middleware de validación de permisos

# Frontend
add(formularios): componente `InputField` reutilizable
add(tabla): lógica de ordenamiento por columnas
add(estilos): variables CSS para tema oscuro

# Testing
add(mocks): mock de servicio de pagos para tests
add(fixtures): datos de prueba para módulo de facturación
```

### 5.5. `wip` - Trabajo en Progreso 🔨

**Qué es:** Checkpoint temporal para guardar trabajo incompleto.

**✅ Cuándo usarlo:**
- Necesitas cambiar de rama/tarea urgentemente.
- Quieres hacer un checkpoint antes de un cambio arriesgado.
- Al final del día para no perder cambios locales.
- Guardas progreso para compartir con el equipo.

**❌ Cuándo NO usarlo:**
- No debe llegar a la rama principal (`main`/`master`).
- Debe reescribirse o convertirse en commits `add` antes del squash.

> [!WARNING]
> Los commits `wip` son temporales. Deben ser reescritos o eliminados antes de crear el PR final.

**Ejemplos:**
```txt
wip: avance en formulario de registro
wip(autenticación): implementación parcial de OAuth2
wip: checkpoint antes de refactor mayor
wip(reportes): gráficos a medio terminar
wip: guardando cambios antes de cambiar de rama
```

### 5.6. `docs` - Documentación

**Qué es:** Cambios en documentación escrita, guías, README, comentarios de código, especificaciones o documentación del código.

**✅ Cuándo usarlo:**
- Actualizar README, añadir guía de contribución, corregir typos en documentación, mejorar comentarios de código que explican algoritmo.
- El cambio es solo texto, imágenes u otros activos de documentación y no modifica código de producción ni pruebas.
- Cuando agregas cualquier tipo de documentación del proyecto.

**❌ Cuándo NO usarlo:**
- No usar para cambios que modifiquen código o comportamiento.

**Ejemplos:**
```txt
# Documentación de proyecto
docs: actualización de `README.md` con instrucciones de instalación
docs: guía de contribución para nuevos desarrolladores
docs: manual de usuario para módulo de facturación

# Documentación técnica
docs(api): especificación OpenAPI para endpoints de productos
docs(arquitectura): diagramas de flujo del sistema
docs(código): JSDoc en funciones de utilidades
```

### 5.7. `style` - Formato de Código

**Qué es:** Cambios que afectan la apariencia del código (formato) sin cambiar la lógica: indentación, espacios, formato, punto y coma, linter autofix.

**✅ Cuándo usarlo:**
- Aplicar prettier/eslint autofix o cualquier herramienta que sólo cambia formato del código.
- Cambios en comentarios de estilo (no su contenido explicativo).

**❌ Cuándo NO usarlo:**
- Si el cambio en formato implicó ajustar código para que funcione diferente o arreglar un bug.

**Ejemplos:**
```txt
style: aplicación de reglas de `ESLint` en todo el proyecto
style: formateo con `Prettier`
style(componentes): corrección de indentación en archivos JSX
style(api): reordenamiento de imports según convención
style: eliminación de espacios en blanco innecesarios
```

### 5.8. `refactor` - Refactorización

**Qué es:** Cambios en el código que no alteran la funcionalidad observable pero mejoran estructura, legibilidad o mantenibilidad.

**✅ Cuándo usarlo:**
- Renombrar variables, extraer funciones, mover módulos, reorganizar archivos, simplificar lógica sin cambiar comportamiento.
- Cambios arquitectónicos internos donde no cambian comportamientos internos.

**❌ Cuándo NO usarlo:**
- Si introduces una nueva funcionalidad.
- Si mejoras rendimiento notablemente.

**Ejemplos:**
```txt
# Backend
refactor(servicios): extracción de lógica común a clase base
refactor(api): división de controlador grande en módulos
refactor(db): migración de queries raw a ORM

# Frontend
refactor(componentes): conversión de clases a hooks
refactor(estado): migración de `Redux` a `Zustand`
refactor(estilos): reorganización de archivos CSS por módulo
```

### 5.9. `test` - Pruebas

**Qué es:** Añadir, modificar o arreglar pruebas automatizadas.

**✅ Cuándo usarlo:**
- Añadir tests para nueva funcionalidad, arreglar tests rotos, mejorar cobertura de prueba, cambiar configuración de test runner.

**❌ Cuándo NO usarlo:**
- No uses para añadir nuevos mocks o fakes que también cambien la lógica de producción.

**Ejemplos:**
```txt
# Tests unitarios
test(servicios): tests para `CustomerService`
test(utilidades): tests para funciones de formateo

# Tests de integración
test(api): tests de integración para endpoint `/orders`
test(autenticación): tests de flujo OAuth completo

# Tests E2E
test(checkout): suite E2E para flujo de compra
test(registro): tests automatizados de formulario de registro

# Configuración de tests
test: configuración de `Jest` para tests asíncronos
test: corrección de mocks desactualizados
```

### 5.10. `chore` - Mantenimiento

**Qué es:** Tareas de mantenimiento que no afectan código de producción ni pruebas directamente (scripts, tareas administrativas, limpieza).

**✅ Cuándo usarlo:**
- Actualizar dependencias de desarrollo (no de producción), scripts build auxiliares, tareas de mantenimiento sin impacto en runtime.
- El cambio no modifica la lógica ejecutada en producción.
- No introduce ni arregla comportamiento que usuarios o sistemas externos percibirían.
- No es una tarea de CI/CD que afecte cómo se construye/despliega el artefacto final.

**❌ Cuándo NO usarlo:**
- No uses para actualizar dependencias que cambian comportamiento de producción.
- Corrige funcionalidades.
- Reescrituras de código o reorganizaciones con impacto en la mantenibilidad/performance.

**Ejemplos:**
```txt
# Dependencias de desarrollo
chore: actualización de `ESLint` a versión 9
chore: actualización de `TypeScript` a 5.x

# Scripts y herramientas
chore: script de limpieza de caché de desarrollo
chore: configuración de `Husky` para pre-commit hooks

# Limpieza
chore: eliminación de archivos temporales del repositorio
chore: actualización de `.gitignore`
```

### 5.11. `ci` - Integración Continua

**Qué es:** Cambios en la configuración de integración continua / pipelines / workflows.

**✅ Cuándo usarlo:**
- Modificar GitHub Actions, GitLab CI, Travis, pipelines de despliegue, variables de CI/CD, jobs de build/test.

**❌ Cuándo NO usarlo:**
- Si el cambio modifica build tools o dependencias del proyecto.

**Ejemplos:**
```txt
# GitHub Actions
ci: workflow para tests en paralelo
ci: job de análisis de código con SonarQube
ci: automatización de releases con semantic-release

# Pipelines
ci: optimización del tiempo de build (caché de dependencias)
ci: stage de despliegue a entorno de staging

# Calidad
ci: integración de reporte de cobertura con Codecov
ci: escaneo de vulnerabilidades en dependencias
```

### 5.12. `build` - Sistema de Build

**Qué es:** Cambios que afectan el sistema de compilación, empaquetado o dependencias que influyen en el artefacto final.

**✅ Cuándo usarlo:**
- Cambiar, actualizar dependencias de producción, modificar Dockerfile que afecta la imagen final.
- Actualizas dependencias cuyos cambios podrían afectar el comportamiento en producción.

**❌ Cuándo NO usarlo:**
- El cambio es exclusivamente sobre pipelines/CI (jobs, secrets, matrix de ejecución) y no modifica el artefacto en sí.

**Ejemplos:**
```txt
# Dependencias de producción
build: actualización de `React` a versión 19
build: actualización de `Django` por parche de seguridad
build: migración de `axios` a `fetch` nativo

# Configuración de build
build(webpack): configuración para tree-shaking
build(vite): optimización de chunks para lazy loading
build: configuración de minificación de CSS

# Docker
build(docker): `Dockerfile` multistage para imagen más ligera
build(docker): actualización de imagen base por seguridad
```

### 5.13. `revert` - Revertir Cambios

**Qué es:** Revertir un commit previo.

**✅ Cuándo usarlo:**
- Revertir un cambio que introdujo un bug o que no debe permanecer por razones operativas, manteniendo historial claro.

**❌ Cuándo NO usarlo:**
- No usar para deshacer trabajo en progreso — si aún no se hizo push, puedes reescribir localmente.

**Ejemplos:**
```txt
revert: reversión de "feat(auth): login con Google"

This reverts commit <hash>.
```

## 🔹 6. Scope

El `scope` indica qué parte del sistema se ve afectada por el cambio. En este proyecto, el scope tiene un rol fundamental: **el flujo de automatización en `release.config.cjs` lo utiliza para ordenar alfabéticamente los commits dentro de cada sección de la release**.

> [!IMPORTANT]
> El scope es **obligatorio** en commits finales (`feat`, `fix`, `perf`) y **opcional** en los casos restantes. Siempre debe representar el **módulo funcional o dominio principal exacto**.

### 6.1. ¿Por qué el Scope debe ser el nombre exacto del módulo?

En el pipeline de publicación ([release.config.cjs](file:///home/theasintota/projects/api-pricut/release.config.cjs)), las notas de la release se organizan por secciones de tipo (`✨ Nuevas Funcionalidades`, `🐛 Corrección de Errores`, `⚡️ Mejoras de Rendimiento`) y dentro de cada sección los commits se ordenan alfabéticamente según su `scope`:

```javascript
context.commitGroups.forEach(group => {
  group.commits.sort((a, b) => {
    const scopeA = a.scope ? a.scope.toLowerCase() : '';
    const scopeB = b.scope ? b.scope.toLowerCase() : '';
    return scopeA.localeCompare(scopeB);
  });
});
```

Si cada desarrollador inventa variantes de scope (por ejemplo `cotizaciones`, `cotizador`, `presupuestos`) o usa nombres de subdirectorios técnicos (`routers`, `services`, `dto`), los cambios quedan dispersos y desorganizados en el changelog. Al usar el **nombre exacto del módulo principal** (`quote_generator`), todos los commits asociados al mismo dominio se agrupan y ordenan de forma natural.

### 6.2. Reglas de Formato del Scope

| Regla | Descripción | Ejemplo |
|-------|-------------|---------|
| **Nombre exacto del módulo** | Debe coincidir exactamente con el nombre del módulo funcional o dominio principal (`src/api/modules/<modulo>`) o módulo raíz transversal (`settings`, `common`, `api`). | `quote_generator`, `settings`, `common` |
| **Granularidad de dominio (No capas técnicas)** | Nunca uses carpetas internas o capas técnicas (`routers`, `services`, `dto`, `models`, `constants`) como scope. El scope siempre es el módulo contenedor. | ✅ `quote_generator`<br>❌ `routers`, `services`, `dto` |
| **Formato idéntico al código** | Mantén el identificador exacto tal como está definido en la arquitectura del proyecto (ej. `quote_generator`). Evita traducciones o alias que fragmenten el changelog. | `quote_generator` (no `cotizaciones` ni `cotizador`) |
| **Sin artículos ni prefijos** | No uses "el", "la", ni agregues palabras adicionales. | `quote_generator` (no `el-quote_generator`) |

### 6.3. Granularidad y Múltiples Módulos

#### ¿Qué ocurre si solo se modifica una subcapa interna?
Si el cambio se realizó exclusivamente en `src/api/modules/quote_generator/routers/`, el `<scope>` **debe seguir siendo `quote_generator`**, nunca `routers`. La granularidad siempre se mantiene a nivel del módulo funcional de negocio.

#### ¿Qué ocurre cuando es necesario modificar varios módulos?
1. **Commits atómicos (Recomendado):** Si los cambios son independientes o pertenecen a responsabilidades distintas, sepáralos en commits diferentes para que cada uno conserve su scope exacto:
   ```bash
   git add src/api/modules/quote_generator/
   git commit -m 'add(quote_generator): endpoint de subida de archivos'

   git add src/api/settings/
   git commit -m 'refactor(settings): inmutabilidad en parámetros de configuración'
   ```
2. **Módulo principal dominante:** Si un cambio en otro módulo (ej. `settings` o `common`) fue realizado exclusivamente para soportar la funcionalidad del módulo principal, se utiliza el scope del módulo dominante:
   ```txt
   add(quote_generator): integración con parámetros de límites de subida
   ```
3. **Cambios transversales a nivel de plataforma:** Si el cambio impacta de forma global a la API o al sistema sin pertenecer a un módulo de negocio particular, utiliza el scope del componente transversal:
   - `api`: Routing general, middlewares globales, ciclo de vida o configuración del servidor FastAPI.
   - `common`: Excepciones base, utilidades transversales o tipos comunes compartidos.
   - `settings`: Configuración y parámetros globales.
4. **Omitir el scope en commits de desarrollo:** En commits intermedios (`add`, `refactor`, `chore`, `wip`), el scope es opcional. Si un commit intermedio abarca varios módulos y ninguno es dominante, se puede omitir el scope.

## 🔹 7. Breaking Change

Cuando un cambio rompe la compatibilidad o modifica el comportamiento esperado, se debe usar la nota **BREAKING CHANGE**. Esto indica que el cambio realizado no es retrocompatible y que, por lo tanto, quienes usen el sistema, librería o servicio deberán adaptar su código o procesos para evitar errores.

> [!IMPORTANT]
> Este tipo de nota implica incrementos de **versión mayor** en el esquema de [versionado semántico (semver)](https://semver.org/lang/es/).

### 7.1. Regla Decisiva

Añade `BREAKING CHANGE` si y solo si el cambio exige alguna de estas tres cosas:

| Criterio | Ejemplo |
|----------|---------|
| Consumidores necesitan cambiar su código/config para seguir funcionando | Cambio en parámetros requeridos |
| La forma, nombre o semántica de una API/contrato cambió | Renombrar campos de respuesta |
| Se eliminó o reemplazó un comportamiento/endpoint/archivo | Eliminar endpoint deprecado |

### 7.2. ¿Dónde y Cómo Indicarlo?

1. **Footer del commit:** Siempre agrega la sección `BREAKING CHANGE: <explicación>`.
2. **Marca el asunto con `!`:** (opcional pero recomendable) `feat(api)!: Cambio en estructura de respuesta`. Herramientas automáticas lo detectan mejor.
3. **Incluye en el body:** Una explicación corta del cambio y en el footer las instrucciones de migración detalladas.

```txt
feat(api)!: cambio en estructura de respuesta del endpoint `/usuarios`

Unificación de nomenclatura de campos y eliminación de wrappers de metadata.

BREAKING CHANGE: el campo `id_usuario` pasa a llamarse `userId`.
Pasos de migración:
1. Actualizar cliente para leer `userId` en lugar de `id_usuario`.
2. Recompilar y desplegar cliente X antes de desplegar servicio Y.
```

Es recomendable acompañar el **BREAKING CHANGE** con una explicación clara de:
- Qué ha cambiado.
- Por qué era necesario modificarlo.
- Qué pasos deben seguir las personas usuarias o el equipo para adaptarse al nuevo comportamiento.

## 🔹 8. Errores Comunes

Evita estos errores frecuentes al escribir commits:

### 8.1. Errores de Redacción

| ❌ Incorrecto | ✅ Correcto | Razón |
|--------------|-------------|-------|
| `Agregar login con Google` | `login con Google OAuth` | Usa frase nominal y minúscula, no imperativo |
| `Corregir el bug de overflow` | `corrección de bug de overflow` | Evita artículos y verbos al inicio |
| `Implementar lazy loading` | `implementación de carga diferida` | Describe QUÉ es, no QUÉ hacer |
| `Actualizar dependencias.` | `actualización de dependencias` | Sin punto final y en minúscula |
| `feat(api): Creación de endpoint` | `feat(api): endpoint de creación` | Inicia en minúscula salvo clases o siglas |
| `add: DTO de usuario` | `add: DTO de usuario` | ✅ Correcto (`DTO` es sigla técnica) |
| `add: CustomerService` | `` add: `CustomerService` `` | Envuelve clases/funciones en backticks |
| `chore: actualización de .gitignore` | `` chore: actualización de `.gitignore` `` | Envuelve rutas o ficheros en backticks |

### 8.2. Errores de Tipo de Commit

| ❌ Incorrecto | ✅ Correcto | Razón |
|--------------|-------------|-------|
| `feat: creación de modelo Product` | `` add: modelo `Product` `` | Es un paso intermedio, no la feature completa |
| `fix: cambio de color de botón` | `style: ajuste de color de botón` | Cambio estético, no es un bug |
| `feat: actualización de dependencias` | `build: actualización de dependencias` | No es funcionalidad nueva |
| `chore: corrección de test roto` | `test: corrección de test unitario` | Es específico de testing |
| `fix: refactorización de función` | `refactor: reorganización de función` | No había bug que corregir |
| `feat: mejora de rendimiento` | `perf: optimización de consultas` | No es funcionalidad, es optimización |

### 8.3. Otros Errores a Evitar

- ❌ **Descripciones vagas:** `fix: Corrección de bug`, `feat: Cosas nuevas`
- ❌ **Commits muy grandes:** Un commit debe hacer una sola cosa
- ❌ **Mezclar tipos:** No combines `feat` + `fix` en el mismo commit
- ❌ **Usar verbos imperativos:** Usa `Adición de` en lugar de `Agregar`
- ❌ **Omitir backticks en código:** Envuelve librerías, funciones, clases, rutas de ficheros, directorios o endpoints entre `` ` ``
- ❌ **Exceder 72 caracteres:** Mantén la descripción concisa
- ❌ **Terminar con punto:** No uses puntuación final