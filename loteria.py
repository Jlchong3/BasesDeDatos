import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import mysql.connector
from mysql.connector import Error

# Funciones de conexión y consulta
def create_connection(host_name, user_name, user_password, db_name, db_port):
    connection = None
    try:
        connection = mysql.connector.connect(
            host=host_name,
            user=user_name,
            passwd=user_password,
            database=db_name,
            port=db_port
        )
        print("Conexión a la base de datos MySQL exitosa")
    except Error as e:
        print(f"Ocurrió el error '{e}'")
    return connection

def obtener_datos(tabla, cursor):
    if tabla is None:
        return None

    consulta_sql = f"SELECT * FROM {tabla}"
    print("Consulta SQL:", consulta_sql)
    
    try:
        cursor.execute(consulta_sql)
        rows = cursor.fetchall()
        columns = [i[0] for i in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        return df
    except mysql.connector.Error as err:
        print(f"Error durante la ejecución de la consulta: {err}")
        return None

# Inicializar la aplicación Dash
app = dash.Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'])

# Conexión a la base de datos
conexion = create_connection("basesloteria.mysql.database.azure.com", "administrador", "@basesloteriaN", "loterianacional", 3306)
cursor = conexion.cursor()

# Diseño de la interfaz gráfica
app.layout = html.Div([
    dcc.Dropdown(
        id='tabla-dropdown',
        options=[
            {'label': 'Tabla de Sucursales', 'value': 'sucursal'},
            {'label': 'Tabla de Ventas', 'value': 'venta'}
        ],
        value='sucursal',
        className='form-control'
    ),
    html.Div(id='tabla-output', className='mt-4'),
])

# Actualizar el contenido de la tabla según la selección del usuario
@app.callback(
    Output('tabla-output', 'children'),
    [Input('tabla-dropdown', 'value')]
)
def actualizar_tabla(tabla_seleccionada):
    try:
        df = obtener_datos(tabla_seleccionada, cursor)
        
        if df is not None:
            return [
                html.Table(
                    id='tabla',
                    children=[
                        # Encabezados de columna
                        html.Thead(
                            html.Tr([html.Th(col) for col in df.columns])
                        ),
                        # Datos de la tabla
                        html.Tbody([
                            html.Tr([
                                html.Td(df.iloc[i][col]) for col in df.columns
                            ]) for i in range(len(df))
                        ])
                    ],
                    className='table table-striped'
                )
            ]
        else:
            return "Error al obtener datos de la tabla."
    except Exception as e:
        print(f"Error en la función actualizar_tabla: {e}")
        return f"Error en la función actualizar_tabla: {e}"

# Ejecutar la aplicación Dash
if __name__ == '__main__':
    app.run_server(debug=True)

# Cerrar la conexión cuando la aplicación Dash se cierra
cursor.close()
conexion.close()