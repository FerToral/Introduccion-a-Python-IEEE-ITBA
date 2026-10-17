"""Recupera auxiliares del curso; comprueba SHA-256 y no sobrescribe."""
from hashlib import sha256
import json
from pathlib import Path
from urllib.request import urlopen

ROOT = Path(__file__).resolve().parents[1]

def preparar():
    datos = json.loads((ROOT / "docs/datos-de-practica.json").read_text(encoding="utf-8"))
    for dato in datos["archivos"]:
        contenido = None
        for relativo in dato["copias"]:
            destino = ROOT / relativo
            if destino.exists():
                if sha256(destino.read_bytes()).hexdigest() != dato["sha256"]:
                    raise ValueError(f"Archivo local diferente: {relativo}; no se sobrescribe")
                continue
            if contenido is None:
                with urlopen(dato["url"], timeout=30) as respuesta:
                    contenido = respuesta.read()
                if sha256(contenido).hexdigest() != dato["sha256"]:
                    raise ValueError(f"Fuente modificada: {dato['nombre']}")
            destino.write_bytes(contenido)
            print("Preparado:", relativo)

if __name__ == "__main__":
    preparar()
