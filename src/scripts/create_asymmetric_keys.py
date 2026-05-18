import asyncio

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ed25519


async def run() -> None:

    # Generar clave privada
    private_key = ed25519.Ed25519PrivateKey.generate()
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )

    # Extraer clave pública
    public_key = private_key.public_key()
    public_bytes = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    )

    private_str = private_bytes.decode(encoding="utf-8")
    public_str = public_bytes.decode(encoding="utf-8")

    print("\n" + "=" * 60)
    print("CLAVES ASIMÉTRICAS (Ed25519) GENERADAS CON ÉXITO")
    print("=" * 60)

    print("\nCLAVE PRIVADA")
    print("Copia y pega el siguiente bloque en tu archivo .env como PRIVATE_KEY:")
    print(private_str.strip())

    print("\nCLAVE PÚBLICA")
    print("Copia y pega el siguiente bloque en tu archivo .env como PUBLIC_KEY:")
    print(public_str.strip())


if __name__ == "__main__":
    asyncio.run(run())
