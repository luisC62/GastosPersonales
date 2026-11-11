"""Exporta los gastos de misgastos.db a un archivo CSV."""

import csv
import sqlite3
import sys
from pathlib import Path

RUTA_BASE_DATOS = "misgastos.db"
COLUMNAS = ["id", "fecha", "cantidad", "tipo", "descripcion"]


def exportar(ruta_csv: Path) -> int:
    """Escribe todos los gastos en el CSV y devuelve cuántos ha exportado."""
    if not Path(RUTA_BASE_DATOS).exists():
        raise FileNotFoundError(f"No existe la base de datos '{RUTA_BASE_DATOS}'.")

    conexion = sqlite3.connect(RUTA_BASE_DATOS)
    try:
        filas = conexion.execute(
            "SELECT id, fecha, cantidad, tipo, descripcion FROM gastos ORDER BY id"
        ).fetchall()
    except sqlite3.OperationalError as error:
        raise ValueError(
            "No se pudo leer la tabla 'gastos'. Comprueba que la base de datos "
            "tiene la tabla esperada."
        ) from error
    finally:
        conexion.close()

    with open(ruta_csv, "w", newline="", encoding="utf-8-sig") as archivo:
        escritor = csv.writer(archivo)
        escritor.writerow(COLUMNAS)
        escritor.writerows(filas)

    return len(filas)


def main() -> None:
    if len(sys.argv) != 2:
        print("Uso: python exportarcsv.py <archivo.csv>", file=sys.stderr)
        sys.exit(1)

    try:
        total = exportar(Path(sys.argv[1]))
    except (OSError, ValueError, sqlite3.Error, csv.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    print(f"Exportados {total} gastos a '{sys.argv[1]}'.")


if __name__ == "__main__":
    main()
