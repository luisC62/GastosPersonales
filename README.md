# Gestor de Gastos

API sencilla hecha con FastAPI y `sqlite3` para registrar gastos personales en euros.
Los gastos se guardan en el fichero `misgastos.db`, que se crea automáticamente la primera vez.
Incluye una web para apuntar y borrar gastos desde el navegador.

## Arrancar el servidor

```powershell
uv sync
uv run uvicorn main:app --reload
```

La documentación interactiva estará disponible en <http://127.0.0.1:8000/docs>,
donde se pueden probar las cinco operaciones sin escribir comandos.

## La web

La carpeta del proyecto tiene una web con solo tres ficheros: `index.html`,
`styles.css` y `app.js` (HTML, CSS y JavaScript, sin frameworks ni compilación).

Para usarla:

1. Arranca el servidor API como se indica arriba.
2. Abre `index.html` con doble clic.

Qué permite hacer la web:

- Registrar un gasto con fecha (por defecto hoy), cantidad en euros, tipo y
  una descripción corta.
- Ver la lista de gastos, del más reciente al más antiguo.
- Ver el total gastado en la semana y en el mes en curso, con su rango de fechas.
- Marcar un gasto de la lista y eliminarlo con el botón «Eliminar seleccionado»
  (pide confirmación antes de borrar).

La web hace sus peticiones a `http://127.0.0.1:8000`, definido en la constante
`URL_API` de `app.js`. Si el servidor no está arrancado, la página muestra un
aviso con el comando necesario para arrancarlo.

El servidor acepta las peticiones de la web aunque se abra como fichero local
(doble clic) gracias al middleware CORS configurado en `main.py`: sin él, el
navegador bloquearía las peticiones por ser de otro origen.

## Peticiones disponibles

| Método | Ruta                      | Qué hace                                      |
|--------|---------------------------|-----------------------------------------------|
| POST   | `/gastos`                 | Crea un gasto y devuelve el gasto con su `id`.|
| GET    | `/gastos`                 | Lista todos los gastos (los más recientes primero). |
| DELETE | `/gastos/{id}`            | Borra el gasto con ese `id`.                  |
| GET    | `/gastos/total-semanal`   | Total gastado en la semana actual (lunes a domingo). |
| GET    | `/gastos/total-mensual`   | Total gastado en el mes natural actual.       |

Los totales se calculan con la fecha actual del servidor e incluyen los gastos
con fecha dentro del periodo, aunque sea posterior a hoy. La respuesta indica
el rango consultado y el importe en euros redondeado a 2 decimales.

Todos los datos viajan en formato JSON. Un gasto tiene estos campos:

- `fecha`: fecha en formato `AAAA-MM-DD`
- `cantidad`: número mayor que 0 (euros)
- `tipo`: texto corto, por ejemplo `comida` o `transporte`
- `descripcion`: texto corto que explica el gasto

## Ejemplos

Crear un gasto:

```powershell
$cuerpo = @{
    fecha = "2026-11-10"
    cantidad = 12.50
    tipo = "comida"
    descripcion = "Menu del dia"
} | ConvertTo-Json

Invoke-RestMethod -Method Post -Uri http://127.0.0.1:8000/gastos `
    -ContentType "application/json" -Body $cuerpo
```

Listar los gastos:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/gastos
```

Borrar el gasto con id 1:

```powershell
Invoke-RestMethod -Method Delete -Uri http://127.0.0.1:8000/gastos/1
```

Consultar el total de la semana actual:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/gastos/total-semanal
```

Respuesta de ejemplo:

```json
{
  "inicio": "2026-11-09",
  "fin": "2026-11-15",
  "total": 31.25
}
```

Consultar el total del mes actual:

```powershell
Invoke-RestMethod -Uri http://127.0.0.1:8000/gastos/total-mensual
```

Respuesta de ejemplo:

```json
{
  "inicio": "2026-11-01",
  "fin": "2026-11-30",
  "total": 132.2
}
```

## Exportar e importar CSV

### Exportar

```powershell
python exportarcsv.py misgastos.csv
```

Crea `misgastos.csv` con una cabecera y todos los gastos:

```csv
id,fecha,cantidad,tipo,descripcion
1,2026-11-10,12.5,comida,Menu del dia
```

El archivo se guarda en UTF-8 (con BOM, para que Excel muestre bien los acentos),
usa comas como separador, fechas `AAAA-MM-DD` y el punto como separador decimal.

### Importar

```powershell
python importarcsv.py misnuevosgastos.csv
```

El CSV debe tener las columnas `fecha`, `cantidad`, `tipo` y `descripcion`.
La columna `id` es opcional y, si aparece, se ignora: SQLite asigna un id nuevo
a cada gasto. Ejemplo:

```csv
fecha,cantidad,tipo,descripcion
2026-11-12,8.9,transporte,Metro
2026-11-13,15.0,comida,Cena
```

El script valida la cabecera y todas las filas antes de insertar. Si algo no
encaja con la tabla `gastos`, muestra un error y no importa ninguna fila.
