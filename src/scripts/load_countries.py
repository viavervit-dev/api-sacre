import asyncio
import json
from typing import Any

from anyio import Path
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.config.database import close_db_pool, create_db_pool, get_db_session
from src.modules.countries.models.country import Country


def __read_fixture_data(file_path: Path) -> dict[str, Any]:
    """Lee el archivo JSON."""

    with open(file_path, encoding="utf-8") as f:
        data: Any = json.load(f)

    return data


async def run(db: AsyncSession, fixtures_dir: Path) -> None:
    """
    Puebla o actualiza la tabla `countries.country` a partir de los archivos JSON de fixtures.

    Lee los archivos JSON en `fixtures_dir`, extrayendo el nombre y código del país a partir del
    nombre de cada archivo (ejemplo: 'Ecuador_EC.json' -> nombre: 'Ecuador', código: 'EC').
    Si el país ya existe en la base de datos (por código o nombre), actualiza sus datos;
    de lo contrario, crea un nuevo registro.
    """

    if not await fixtures_dir.exists() or not await fixtures_dir.is_dir():
        raise ValueError(
            f"El directorio de fixtures '{fixtures_dir}' no existe o no es un directorio."
        )

    json_files = sorted([file async for file in fixtures_dir.glob("*.json")])

    if not json_files:
        raise ValueError(f"No se encontraron archivos JSON en '{fixtures_dir}'.")

    processed_count = 0

    for file_path in json_files:
        stem = file_path.stem

        if "_" not in stem:
            raise ValueError(
                f"Advertencia: El archivo '{file_path.name}' no cumple con el formato "
                f"'<Nombre>_<CODIGO>.json'. Se omite."
            )

        raw_name, code = stem.rsplit("_", maxsplit=1)
        country_name = raw_name.replace("_", " ").strip()
        country_code = code.strip().upper()
        administrative_structure = await asyncio.to_thread(__read_fixture_data, file_path)

        # Verificar si el país ya existe (por código o por nombre)
        stmt = select(Country).where(
            (Country.code == country_code) | (Country.name == country_name)
        )
        result = await db.execute(stmt)
        country = result.scalar_one_or_none()

        if country:
            country.name = country_name
            country.code = country_code
            country.administrative_structure = administrative_structure
        else:
            country = Country(
                name=country_name,
                code=country_code,
                administrative_structure=administrative_structure,
            )
            db.add(country)

        await db.flush()
        processed_count += 1

    await db.commit()

    print(f"Proceso finalizado, total de países procesados: {processed_count}.")


async def main() -> None:

    fixtures_dir = (
        (await Path(__file__).resolve()).parent.parent / "modules" / "countries" / "fixtures"
    )

    await create_db_pool()

    try:
        async for db in get_db_session():
            await run(db=db, fixtures_dir=fixtures_dir)
    except Exception as e:
        print(f"Ocurrió un error inesperado: {e}")
    finally:
        await close_db_pool()


if __name__ == "__main__":
    asyncio.run(main())
