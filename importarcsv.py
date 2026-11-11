"""Importa gastos desde un archivo CSV a misgastos.db."""

import csv
import math
import sqlite3
import sys
from datetime import date
from pathlib import Path

RUTA_BASE_DATOS = "misgastos.db"
COLUMNAS_OBLIGATORIAS = ["fecha", "cantidad", "tipo", "descripcion"]
COLUMNAS_OPCIONALES = {"id"}
COLUMNAS_TABLA = ["id", "fecha", "cantidad", "tipo", "descripcion"]
LONGITUD_MAXIMA_TIPO = 50
LONGITUD_MAXIMA_DESCRIPCION = 200


def validar_cabecera(columnas: list[str] | None) -> None:
    """Comprueba que la cabecera del CSV tenga las columnas necesarias."""
    if not columnas:
        raise ValueError("El CSV está vacío o no tiene fila de cabecera.")

    if len(columnas) != len(set(columnas)):
        raise ValueError("La cabecera del CSV tiene columnas repetidas.")

    permitidas = set(COLUMNAS_OBLIGATORIAS) | COLUMNAS_OPCIONALES
    desconocidas = [columna for columna in columnas if columna not in permitidas]
    if desconocidas:
        raise ValueError(
            "La cabecera del CSV tiene columnas no válidas: "
            + ", ".join(desconocidas)
        )

    faltantes = [
        columna for columna in COLUMNAS_OBLIGATORIAS if columna not in columnas
    ]
    if faltantes:
        raise ValueError(
            "Faltan columnas obligatorias en el CSV: " + ", ".join(faltantes)
        )


def validar_fila(fila: dict, numero: int) -> tuple[str, float, str, str]:
    """Valida una fila y devuelve los valores listos para guardar."""
    if None in fila:
        raise ValueError(f"Fila {numero}: tiene más valores que columnas.")

    fecha_texto = (fila.get("fecha") or "").strip()
    try:
        fecha = date.fromisoformat(fecha_texto)
    except ValueError:
        raise ValueError(
            f"Fila {numero}: la fecha '{fecha_texto}' no es válida "
            "(usa el formato AAAA-MM-DD)."
        ) from None
    if fecha.isoformat() != fecha_texto:
        raise ValueError(
            f"Fila {numero}: la fecha '{fecha_texto}' debe tener el formato "
            "AAAA-MM-DD."
        )

    cantidad_texto = (fila.get("cantidad") or "").strip()
    try:
        cantidad = float(cantidad_texto)
    except ValueError:
        raise ValueError(
            f"Fila {numero}: la cantidad '{cantidad_texto}' no es un número."
        ) from None
    if not math.isfinite(cantidad) or cantidad <= 0:
        raise ValueError(f"Fila {numero}: la cantidad debe ser mayor que 0.")

    tipo = (fila.get("tipo") or "").strip()
    if not tipo:
        raise ValueError(f"Fila {numero}: el tipo no puede estar vacío.")
    if len(tipo) > LONGITUD_MAXIMA_TIPO:
        raise ValueError(
            f"Fila {numero}: el tipo no puede superar "
            f"{LONGITUD_MAXIMA_TIPO} caracteres."
        )

    descripcion = (fila.get("descripcion") or "").strip()
    if not descripcion:
        raise ValueError(f"Fila {numero}: la descripción no puede estar vacía.")
    if len(descripcion) > LONGITUD_MAXIMA_DESCRIPCION:
        raise ValueError(
            f"Fila {numero}: la descripción no puede superar "
            f"{LONGITUD_MAXIMA_DESCRIPCION} caracteres."
        )

    return fecha.isoformat(), cantidad, tipo, descripcion


def leer_gastos(ruta_csv: Path) -> list[tuple[str, float, str, str]]:
    """Lee y valida todas las filas antes de tocar la base de datos."""
    with open(ruta_csv, newline="", encoding="utf-8-sig") as archivo:
        lector = csv.DictReader(archivo)
        validar_cabecera(lector.fieldnames)
        gastos = [
            validar_fila(fila, numero) for numero, fila in enumerate(lector, start=2)
        ]

    if not gastos:
        raise ValueError("El CSV no contiene gastos que importar.")

    return gastos


def importar(ruta_csv: Path) -> int:
    """Importa los gastos del CSV y devuelve cuántos ha insertado."""
    if not ruta_csv.exists():
        raise FileNotFoundError(f"No existe el archivo '{ruta_csv}'.")
    if not Path(RUTA_BASE_DATOS).exists():
        raise FileNotFoundError(f"No existe la base de datos '{RUTA_BASE_DATOS}'.")

    gastos = leer_gastos(ruta_csv)

    conexion = sqlite3.connect(RUTA_BASE_DATOS)
    try:
        columnas_bd = {
            fila[1] for fila in conexion.execute("PRAGMA table_info(gastos)").fetchall()
        }
        if not columnas_bd:
            raise ValueError("La base de datos no tiene la tabla 'gastos'.")

        faltantes = [
            columna for columna in COLUMNAS_TABLA if columna not in columnas_bd
        ]
        if faltantes:
            raise ValueError(
                "La tabla 'gastos' no tiene las columnas esperadas: "
                + ", ".join(faltantes)
            )

        conexion.executemany(
            "INSERT INTO gastos (fecha, cantidad, tipo, descripcion) "
            "VALUES (?, ?, ?, ?)",
            gastos,
        )
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()

    return len(gastos)


def main() -> None:
    if len(sys.argv) != 2:
        print("Uso: python importarcsv.py <archivo.csv>", file=sys.stderr)
        sys.exit(1)

    try:
        total = importar(Path(sys.argv[1]))
    except (OSError, ValueError, sqlite3.Error, csv.Error) as error:
        print(f"Error: {error}", file=sys.stderr)
        sys.exit(1)

    print(f"Importados {total} gastos desde '{sys.argv[1]}'.")


if __name__ == "__main__":
    main()
