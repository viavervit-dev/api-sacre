from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

# Directorio base de los módulos: src/api/modules
MODULES_DIR = Path(__file__).resolve().parents[1] / "modules"

# Detecta automáticamente todas las carpetas 'templates' existentes en los módulos
template_directories = [
    template_dir for template_dir in MODULES_DIR.glob("*/templates") if template_dir.is_dir()
]

# Singleton global del entorno de Jinja
jinja_env = Environment(
    loader=FileSystemLoader(searchpath=template_directories),
    autoescape=select_autoescape(enabled_extensions=["html", "xml"]),
    trim_blocks=True,
    lstrip_blocks=True,
)
