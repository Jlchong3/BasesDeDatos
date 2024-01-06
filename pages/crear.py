import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import mysql.connector
from mysql.connector import Error
from app import app
from app import cursor

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


layout = dbc.Container([
    html.Div([
        dcc.Dropdown(
            id='tabla-dropdown',
            options=[
                {'label': 'Tabla de Sucursales', 'value': 'sucursal'},
                {'label': 'Tabla de Ventas', 'value': 'venta'}
            ],
            value='sucursal',
            className='form-control',
        ),
        html.Div(id='tabla-output', className='mt-4'),
        ],
        style= {'marginTop':'1vh'}
    )
])

# Actualizar el contenido de la tabla según la selección del usuario
@app.callback(
    Output('tabla-output', 'children'),
    [Input('tabla-dropdown', 'value')]
)
def actualizar_tabla(tabla_seleccionada):
    try:
        df = obtener_datos(tabla_seleccionada, cursor)
        if df is None:
            return "Error al obtener datos de la tabla."
        return html.Table(
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
    except Exception as e:
        print(f"Error en la función actualizar_tabla: {e}")
        return f"Error en la función actualizar_tabla: {e}"

