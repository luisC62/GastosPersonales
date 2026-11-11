## AGENTS.md - Gestor de Gastos
Servidor API diseñada para controlar los gastos personales. 
Web front end para comunicar con el servidor y realizar operaciones con los gastos.
## Stack y estructura
- El servidor API sólo se programará en Python, utilizando fundamentalmente las librería FastAPI y sqlite3.
- La aplicación web hará peticiones de creación, borrado y listado de gastos, y de los totales semanal y mensual. No utilizará frameworks ni ninguna otra tecnología que no sea HTML, CSS y JavaScript. Constará solamente de los ficheros `index.html`, `styles.css` y `app.js`. Al abrir la página index.html se cargan todos los gastos y los totales de la semana y del mes, y se listan.
## Convenciones
- Textos de la interfaz en español.
- Código simple, nombres descriptivos y comentarios solo donde aporten.
- Diseño limpio y responsive; cualquier pantalla nueva debe verse bien en el móvil.
## Datos
- Los registros de gastos se almacenaran en el archivo misgastors.db, manejado por la librería sqlite3.
- Los datos a almacenar seran: La fecha del gasto, la cantidad en euros, el tipo de gasto una descriptción corta del gasto.
## Fechas
El servidor API utiliza librería `datetime`.
## Moneda
La moneda para los gastos será siempre euros.
## Totales semana y mes
La API proporcionará el total gastado en la semana y el mes en curso.
- La semana va de lunes a domingo.
- El mes es el mes natural, del día 1 al último día.
- Se calculan con la fecha actual del servidor y se incluye todo gasto con fecha dentro del periodo, aunque sea posterior a hoy.
- La respuesta indica el rango de fechas y el total en euros redondeado a 2 decimales; sin gastos, el total es 0.
## Forma de trabajar
- Haz solo lo que se pide: no añadas funcionalidades por tu cuenta.
- Cambios pequeños y enfocados; no reescribas lo que ya funciona.
- Al terminar, resume qué has cambiado y cualquier decisión que deba revisar.
## Memoria
- Al empezar, lee `MEMORY.md` para conocer el estado del proyecto y las decisiones tomadas.
- Al terminar una tarea, actualízalo: estado actual, decisiones importantes (con su porqué) y errores a evitar.
- Mantenlo breve (máximo ~50 líneas): resume o elimina lo que ya no aporte.
- Si algo se convierte en una regla permanente, propón moverlo a `AGENTS.md` en lugar de dejarlo en la memoria.
- No guardes nunca datos sensibles (claves, tokens, datos personales).
## Límites
- ✅ Siempre: respetar las reglas de fechas, mantener los textos en español.
- ⚠️ Pregunta antes: crear archivos nuevos, cambiar el formato de los datos guardados.
- 🚫 Nunca: añadir dependencias, frameworks o un paso de build.
- ✅ Siempre: actualizar `MEMORY.md` al terminar cada tarea.