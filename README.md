# Aplicación web Dash con MySQL - CRUD

Este proyecto demuestra una aplicación web simple de CRUD (Crear, Leer, Actualizar, Eliminar) utilizando Dash, un marco web de Python, y MySQL como base de datos en el backend. La aplicación permite a los usuarios realizar varias operaciones en tablas dentro de la base de datos 'loterianacional'.

## Tabla de Contenidos

- [Configuración](#configuración)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Características](#características)
- [Uso](#uso)
- [Dependencias](#dependencias)
- [Contribuir](#contribuir)
- [Licencia](#licencia)

## Configuración

1. Clonar el repositorio:

   ```bash
   git clone https://github.com/Jlchong3/BasesDeDatos
   cd BasesDeDatos
   ```

2. Instalar las dependencias necesarias:

   ```bash
   pip install -r requirements.txt
   ```

3. Configurar los detalles de conexión de MySQL:

   Actualiza la función `create_connection` en `app.py` con los detalles de tu servidor MySQL:

   ```python
   conexion = create_connection(
       "basesloteria.mysql.database.azure.com",
       "tu_usuario_mysql",
       "tu_contraseña_mysql",
       "loterianacional",
       3306
   )
   ```

4. Ejecutar la aplicación:

   ```bash
   python index.py
   ```

   Visita [http://127.0.0.1:8050/](http://127.0.0.1:8050/) en tu navegador para acceder a la aplicación web.

## Estructura del Proyecto

El proyecto está organizado de la siguiente manera:

- `app.py`: Contiene la configuración principal de la aplicación Dash, funciones de conexión a la base de datos y funciones de recuperación de datos.
- `index.py`: Inicializa la aplicación Dash y define el diseño principal con la navegación.
- `pages/`: Directorio que contiene módulos separados para cada operación de CRUD (crear, leer, actualizar, eliminar).
- `assets/`: Directorio para almacenar activos estáticos, como imágenes o hojas de estilo.

## Características

1. **Navegación:**
   - La aplicación proporciona una barra de navegación con opciones para crear, leer, actualizar y eliminar registros.

2. **Operaciones de CRUD:**
   - Crear: Los usuarios pueden agregar nuevos registros a la base de datos.
   - Leer: Los usuarios pueden ver los datos de las tablas seleccionadas y aplicar filtros (cláusulas WHERE y ORDER BY).
   - Actualizar: Los usuarios pueden modificar registros existentes en la base de datos.
   - Eliminar: Los usuarios pueden eliminar registros de la base de datos.

3. **Tablas Dinámicas:**
   - La aplicación muestra dinámicamente tablas según la selección e input del usuario.

## Uso

1. **Crear:**
   - Navega a la página "Crear" para agregar nuevos registros a la tabla seleccionada.

2. **Leer:**
   - Navega a la página "Consultar" para ver datos de la tabla seleccionada. Aplica filtros utilizando cláusulas WHERE y ORDER BY.

3. **Actualizar:**
   - Navega a la página "Actualizar" para modificar registros existentes en la tabla seleccionada.

4. **Eliminar:**
   - Navega a la página "Eliminar" para eliminar registros de la tabla seleccionada.

## Dependencias

- Dash: Marco web para construir aplicaciones web analíticas.
- Dash Bootstrap Components: Componentes para construir aplicaciones Dash con estilo Bootstrap.
- MySQL Connector: Controlador de Python para MySQL.

## Contribuir

Siéntete libre de contribuir al proyecto abriendo problemas o enviando solicitudes de extracción. Tu retroalimentación y contribuciones son muy apreciadas.

## Licencia

Este proyecto está bajo la Licencia MIT; consulta el archivo [LICENSE](LICENSE) para más detalles.
