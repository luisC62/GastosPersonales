## Rol
Actúa como desarrollador frontend senior que escribe código simple, claro y fácil de entender para alguien que está empezando a programar.

## Contexto
Quiero crear desde cero "Control de gastos", una web que registrará gastos personales. Se podrá introducir un gasto indicando la fecha, el tipo de gasto, y una breve descripción del gasto. Se almacenarán en la base de datos `misgastos.db` y para ello se realizarán peticiones a la API programada en Python.

## Tarea
Crea la web con estas funcionalidades:
1. Un formulario para registrar una gastos con:
- Fecha (por defecto hoy, pero editable para poder apuntar días anteriores)
- Tipo
- Breve descripción
2. La lista de gastos, del más reciente al más antiguo.
3. Los datos introducidos seran guardados en la base de sqlite3, `misgastos.db`.
4. La posibilidad de eliminar un gasto seleccionandolo de la lista de gastos.

## Restricciones y reglas
- La moneda de los gastos siempre será en euros.
- Usa siempre la fecha local del usuario, nunca UTC.
Técnicas:
- HTML, CSS y JavaScript, sin frameworks, sin librerías y sin compilar nada.
- Solo tres archivos: index.html, styles.css y app.js.
- Tiene que funcionar abriendo index.html con doble clic. Se tiene que haber arrancado previamente el servidor API.
- Al abrir la index.html, se carga la lista de gastos automáticamente.
- Si no se ha arrancado el servidor, informar al usuario.
- No añadas nada que no aparezca en este mensaje.
- Diseño limpio y moderno, que se vea bien en el móvil.
- Todos los textos de la interfaz en español.

## Formato de salida
1. Crea los tres archivos directamente en la carpeta del proyecto.
2. Al terminar, responde con:
- Un resumen de 3-4 líneas de lo que has creado.
- Los pasos para probarlo.
- Cualquier decisión que hayas tomado por tu cuenta y que yo deba revisar.

## Documentación
Actualiza los archivos README.md y MEMORY.md. 