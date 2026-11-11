### Script de exportación
Construye un script en python que exporte el contenido del archivo `misgastos.db`, manejado por sqlite3, a un archivo csv.
El nombre del nuevo script será: `exportarcsv.py` y funcionará de la siguiete manera a modo de ejemplo:
```
python exportarcsv.py misgastos.csv
```
Siendo `misgastos.csv` el nuevo fichero creado por el script.

### Script de importación
De la misma manera, construye un script en python que importe el contenido de un archivo csv al archivo de sqlite3 `misgastos.db`. Si los datos no encajaran con la tabla de sqlite3, se emitiría un error.
El nombre del nuevo script sera `importarcsv.py` y funcionará de la siguiete manera a modo de ejemplo:
```
python importarcsv.py misnuevosgastos.csv
```
Siendo `misnuevosgastos.csv` el fichero de formato csv con los nuevos gastos.

### Documentación
Actualiza los archivos README.md y MEMORY.md. 