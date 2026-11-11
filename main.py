import sqlite3
from contextlib import asynccontextmanager, contextmanager
from datetime import date, timedelta

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

# Nombre del fichero donde se guardan los gastos.
RUTA_BASE_DATOS = "misgastos.db"


@contextmanager
def abrir_base_datos():
    """Abre una conexión con SQLite y la cierra al terminar."""
    conexion = sqlite3.connect(RUTA_BASE_DATOS)
    conexion.row_factory = sqlite3.Row  # Permite leer las columnas por su nombre.
    try:
        yield conexion
        conexion.commit()
    finally:
        conexion.close()


def crear_tabla():
    """Crea la tabla de gastos si todavía no existe."""
    with abrir_base_datos() as conexion:
        conexion.execute(
            """
            CREATE TABLE IF NOT EXISTS gastos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                fecha TEXT NOT NULL,
                cantidad REAL NOT NULL,
                tipo TEXT NOT NULL,
                descripcion TEXT NOT NULL
            )
            """
        )


def rango_semana(hoy: date) -> tuple[date, date]:
    """Devuelve el lunes y el domingo de la semana de `hoy`."""
    lunes = hoy - timedelta(days=hoy.weekday())
    return lunes, lunes + timedelta(days=6)


def rango_mes(hoy: date) -> tuple[date, date]:
    """Devuelve el primer y el último día del mes de `hoy`."""
    primer_dia = hoy.replace(day=1)
    if hoy.month == 12:
        siguiente_mes = date(hoy.year + 1, 1, 1)
    else:
        siguiente_mes = date(hoy.year, hoy.month + 1, 1)
    return primer_dia, siguiente_mes - timedelta(days=1)


def sumar_gastos(conexion: sqlite3.Connection, inicio: date, fin: date) -> float:
    """Suma los gastos con fecha entre `inicio` y `fin`, ambos incluidos."""
    fila = conexion.execute(
        "SELECT COALESCE(SUM(cantidad), 0) AS total FROM gastos WHERE fecha BETWEEN ? AND ?",
        (inicio.isoformat(), fin.isoformat()),
    ).fetchone()
    return round(fila["total"], 2)


def calcular_total(inicio: date, fin: date) -> dict:
    """Devuelve el total gastado en el periodo indicado."""
    with abrir_base_datos() as conexion:
        total = sumar_gastos(conexion, inicio, fin)
    return {"inicio": inicio, "fin": fin, "total": total}


@asynccontextmanager
async def ciclo_de_vida(app: FastAPI):
    # Al arrancar el servidor nos aseguramos de que la tabla exista.
    crear_tabla()
    yield


app = FastAPI(title="Gestor de Gastos", lifespan=ciclo_de_vida)

# La web (index.html) se abre directamente con doble clic, así que el navegador
# la considera origen "null". Sin este middleware el navegador bloquearía las
# peticiones de la web a la API por ser de otro origen.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


class GastoEntrada(BaseModel):
    """Datos que envía el cliente para crear un gasto."""

    fecha: date = Field(description="Fecha del gasto (AAAA-MM-DD)")
    cantidad: float = Field(gt=0, description="Cantidad en euros")
    tipo: str = Field(min_length=1, max_length=50, description="Tipo de gasto")
    descripcion: str = Field(
        min_length=1, max_length=200, description="Descripción corta del gasto"
    )


class Gasto(GastoEntrada):
    """Gasto tal y como lo devuelve la API, con su id."""

    id: int


class TotalPeriodo(BaseModel):
    """Total gastado en un periodo, con sus fechas de inicio y fin."""

    inicio: date = Field(description="Primer día del periodo")
    fin: date = Field(description="Último día del periodo")
    total: float = Field(description="Total gastado en euros")


@app.post("/gastos", response_model=Gasto, status_code=201)
def crear_gasto(gasto: GastoEntrada):
    """Registra un gasto nuevo y devuelve el gasto con su id."""
    with abrir_base_datos() as conexion:
        cursor = conexion.execute(
            "INSERT INTO gastos (fecha, cantidad, tipo, descripcion) VALUES (?, ?, ?, ?)",
            (
                gasto.fecha.isoformat(),
                gasto.cantidad,
                gasto.tipo,
                gasto.descripcion,
            ),
        )
        fila = conexion.execute(
            "SELECT * FROM gastos WHERE id = ?", (cursor.lastrowid,)
        ).fetchone()

    return dict(fila)


@app.get("/gastos", response_model=list[Gasto])
def listar_gastos():
    """Devuelve todos los gastos, primero los más recientes."""
    with abrir_base_datos() as conexion:
        filas = conexion.execute(
            "SELECT * FROM gastos ORDER BY fecha DESC, id DESC"
        ).fetchall()

    return [dict(fila) for fila in filas]


@app.get("/gastos/total-semanal", response_model=TotalPeriodo)
def total_semanal():
    """Devuelve el total gastado en la semana actual (lunes a domingo)."""
    inicio, fin = rango_semana(date.today())
    return calcular_total(inicio, fin)


@app.get("/gastos/total-mensual", response_model=TotalPeriodo)
def total_mensual():
    """Devuelve el total gastado en el mes natural actual."""
    inicio, fin = rango_mes(date.today())
    return calcular_total(inicio, fin)


@app.delete("/gastos/{gasto_id}")
def borrar_gasto(gasto_id: int):
    """Borra el gasto indicado por su id."""
    with abrir_base_datos() as conexion:
        cursor = conexion.execute("DELETE FROM gastos WHERE id = ?", (gasto_id,))
        if cursor.rowcount == 0:
            raise HTTPException(
                status_code=404,
                detail=f"No existe ningún gasto con el id {gasto_id}",
            )

    return {"mensaje": f"Gasto {gasto_id} borrado correctamente"}

"""Arrancar el servidor con el siguiente comando: uv run uvicorn main:app --reload"""
