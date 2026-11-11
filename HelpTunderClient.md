#### Explica como probar las peticiones utilizando la extensión Thunder Client en Visual Code Studio.

1. Antes de empezar
Ten el servidor arrancado en una terminal:
uv run uvicorn main:app --reload
Y comprueba que responde en http://127.0.0.1:8000/docs.
Instala la extensión si no la tienes:
1. En VS Code pulsa Ctrl + Shift + X (panel de extensiones).
2. Busca Thunder Client (de Rangav).
3. Pulsa Install.
2. Abrir Thunder Client
- Aparece un icono con forma de rayo en la barra lateral izquierda.
- Pulsa en él y luego en New Request.
- Verás una barra con el método (GET, POST, etc.), la URL y el botón Send.
3. Crear un gasto (POST)
1. Cambia el método a POST.
2. Escribe la URL:
http://127.0.0.1:8000/gastos
3. Ve a la pestaña Body y selecciona JSON.
4. Pega este contenido:
{
  "fecha": "2026-11-10",
  "cantidad": 15.75,
  "tipo": "comida",
  "descripcion": "Cena"
}
5. Pulsa Send.
Deberías recibir un estado 201 Created y una respuesta parecida a:
{
  "fecha": "2026-11-10",
  "cantidad": 15.75,
  "tipo": "comida",
  "descripcion": "Cena",
  "id": 3
}
Apunta el id que devuelve, porque lo necesitarás para borrarlo.
4. Listar todos los gastos (GET)
1. Pulsa New Request (o cambia el método de la petición actual).
2. Método: GET.
3. URL:
http://127.0.0.1:8000/gastos
4. Pulsa Send.
Verás un estado 200 OK y un array JSON con todos los gastos, por ejemplo:
[
  {
    "fecha": "2026-11-10",
    "cantidad": 15.75,
    "tipo": "comida",
    "descripcion": "Cena",
    "id": 3
  },
  {
    "fecha": "2026-11-10",
    "cantidad": 12.5,
    "tipo": "comida",
    "descripcion": "Menú del día",
    "id": 1
  }
]
5. Borrar un gasto (DELETE)
1. Crea otra petición.
2. Método: DELETE.
3. URL (sustituye 3 por el id que quieras borrar):
http://127.0.0.1:8000/gastos/3
4. Pulsa Send.
Respuesta esperada (200 OK):
{
  "mensaje": "Gasto 3 borrado correctamente"
}
Si envías otra vez la misma petición, recibirás 404 Not Found porque ya no existe.
6. Consultar el total de la semana (GET)
1. Crea otra petición.
2. Método: GET.
3. URL:
http://127.0.0.1:8000/gastos/total-semanal
4. Pulsa Send.
Verás un estado 200 OK y un JSON con el rango de fechas y el total, por ejemplo:
{
  "inicio": "2026-11-09",
  "fin": "2026-11-15",
  "total": 31.25
}
La semana siempre empieza en lunes y termina en domingo.
7. Consultar el total del mes (GET)
1. Crea otra petición.
2. Método: GET.
3. URL:
http://127.0.0.1:8000/gastos/total-mensual
4. Pulsa Send.
Verás un estado 200 OK y un JSON con el rango de fechas y el total, por ejemplo:
{
  "inicio": "2026-11-01",
  "fin": "2026-11-30",
  "total": 132.2
}
8. Guardar las peticiones (opcional)
Para no escribir las URLs cada vez:
1. En Thunder Client, pulsa Collections en la barra lateral.
2. Crea una colección, por ejemplo Gestor de Gastos.
3. Con una petición abierta, pulsa el icono de guardar y elige esa colección.
4. Repite con las cinco peticiones para tenerlas siempre a mano.
9. Consejos rápidos
- En la pestaña Response puedes ver el estado, el tiempo y el JSON con formato.
- Si ves un error de conexión, comprueba que el servidor sigue arrancado en el puerto 8000.
- Puedes probar datos inválidos, por ejemplo "cantidad": 0: la API responderá 422 indicando que la cantidad debe ser mayor que 0.
- No hace falta añadir la cabecera Content-Type a mano: al elegir JSON en el Body, Thunder Client la añade automáticamente.