import sys

import toml  # type: ignore[import-untyped]  # pyright: ignore[reportMissingModuleSource]

if len(sys.argv) < 2:
    print("Uso: python update_version.py <nueva_version>")
    sys.exit(1)

new_version = sys.argv[1]
pyproject_file = "pyproject.toml"

with open(pyproject_file, encoding="utf-8") as f:
    data = toml.load(f)

# Actualiza solo la versión del proyecto en la sección de poetry
if "tool" in data and "poetry" in data["tool"]:
    data["tool"]["poetry"]["version"] = new_version
else:
    print("No se encuentra la sección [tool.poetry] en pyproject.toml")
    sys.exit(1)

with open(pyproject_file, "w", encoding="utf-8") as f:
    toml.dump(data, f)

print(f"pyproject.toml actualizado a la versión {new_version}")
