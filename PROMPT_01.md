## Rol
Actúa como desarrollador backend senior que escribe código simple, claro y fácil de entender para alguien que está empezando a programar.

## Contexto
Quiero crear desde cero un gestor de gastos, un servicio api para registrar mis gastos personales. sta es la primera versión y tiene que ser muy simple.

## Tarea
En Python, crea un servidor API para registrar los gastos personales en el fichero `misgastos.db` con la librería sqlite3. El servidor se desarrollará con la libería FastAPI y contemplará las siguientes peticiones:
1. Creación de un gasto
2. Borrado de un gasto.
3. Listado de todos los gastos.

## Restricciones y reglas
1. Las peticiones y las respuestas utilizarán el formato JSON.
2. Los gastos se almacenarán en el fichero `misgastos.db` y constarán de los campos de fecha del gasto, cantidad en euros, tipo de gasto, y breve descripción del gasto.

## Formato de salida
1. Crea los archivos necesarios directamente en la carpeta del proyecto.
2. Al terminar, responde con:
- Un resumen de 3-4 líneas de lo que has creado.
- Los pasos para probarlo.
- Cualquier decisión que hayas tomado por tu cuenta y que yo deba revisar.
- Un ejemplo de utilización de la aplicación.