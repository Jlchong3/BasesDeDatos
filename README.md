# Loteria Nacional Base de Datos

## Resumen

Este script en Python proporciona una interfaz de línea de comandos para gestionar registros en una base de datos MySQL alojada en Azure. El script permite a los usuarios realizar diversas operaciones, como agregar, eliminar y editar registros, así como realizar consultas de datos. Utiliza la biblioteca `pandas` para la visualización tabular y la biblioteca `mysql-connector` para la conexión a la base de datos.

## Requisitos previos

Antes de ejecutar el script, asegúrate de tener lo siguiente instalado:

- Python (versión 3.x)
- Biblioteca pandas (`pip install pandas`)
- Biblioteca mysql-connector (`pip install mysql-connector-python`)

## Configuración

Actualiza los detalles de conexión a la base de datos en el script:

```python
conn = sql.connect(
    host = "basesloteria.mysql.database.azure.com",
    user = "administrador",
    password = "@basesloteriaN",
    database = "loterianacional",
    autocommit=True
)
```

## Uso

1. Ejecuta el script en un entorno de Python:

   ```bash
   python script.py
   ```

2. El script mostrará las tablas disponibles en la base de datos conectada.

3. Elige una opción del menú (1 al 5) para realizar la operación deseada:

   - **Opción 1: Agregar Registro**
     - Permite a los usuarios agregar un nuevo registro a una tabla seleccionada.

   - **Opción 2: Eliminar Registro**
     - Permite a los usuarios eliminar un registro de una tabla seleccionada. El script solicita los valores de las columnas clave primaria.

   - **Opción 3: Editar Registro**
     - Permite a los usuarios editar un registro existente en una tabla seleccionada. Se solicita a los usuarios que ingresen nuevos valores para cada columna.

   - **Opción 4: Consultar Registro**
     - Realiza una consulta simple en una tabla seleccionada basada en un valor proporcionado de la clave primaria.

   - **Opción 5: Salir**
     - Termina el script.

## Información Adicional

- El script utiliza manejo de excepciones para abordar errores durante las operaciones en la base de datos.

- Se emplea la biblioteca `pandas` para mostrar el contenido de la tabla en formato tabular.

- El script asegura el cierre adecuado del cursor de la base de datos.

Esta aplicacion aun esta en prototipo y pronto se la implementara como pagina web
