import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import mysql.connector
from mysql.connector import Error
from pandas.io.formats.printing import justify
from app import app
from app import cursor
from app import obtener_datos

cursor.execute("SHOW TABLES")
table_names = [i[0] for i in cursor.fetchall()]

where_group = dbc.InputGroup(
    [
        dbc.InputGroupText("WHERE"),
        dbc.Input(id="where",type='text', placeholder="ej: nombre = 'Laura'"),
    ]
)

orderby_group = dbc.InputGroup(
    [
        dbc.InputGroupText("ORDER BY"),
        dbc.Input(id="orderby",type='text', placeholder="ej: nombre"),
    ]
)


layout = dbc.Container([
    html.Div([
        dcc.Dropdown(
            id='tabla-dropdown',
            options=[{'label': f'Tabla de {table}', 'value': table} for table in table_names],
            value= table_names[0],
            className='form-control',
        ),
        html.Div(id='tabla-output', className='mt-4'),
        ],
        style= {'marginTop':'1vh'}
    ),
    html.Br(),
    html.Div([where_group, orderby_group]),
    html.Br(),
    html.Div(dbc.Button("Execute", id="boton", n_clicks = 0), style = {"display":"flex","justifyContent":"center"})
])


# Actualizar el contenido de la tabla según la selección del usuario
@app.callback(
    Output('tabla-output', 'children'),
    [Input('tabla-dropdown', 'value'),
     State('where','value'),
     State('orderby','value'),
     Input('boton', 'n_clicks')]
)
def consultar_tabla(tabla_seleccionada, where, orderby, n):
    try:
        df = obtener_datos(tabla_seleccionada, cursor, where, orderby)
        if df is None:
            return html.Div(html.P(f"Error en la función actualizar_tabla", style={"textAlign":"center","color":"red","fontWeight":"bold"}), 
                            style = {"display":"flex","justifyContent":"center"})
        return html.Table(
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
        return html.Div(html.P(f"Error en la función actualizar_tabla: {e}", style={"textAlign":"center","color":"red","fontWeight":"bold"}), 
                        style = {"display":"flex","justifyContent":"center"})
