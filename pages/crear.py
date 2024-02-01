import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
from app import app
from app import cursor
from app import obtener_datos

cursor.execute("SHOW TABLES")
table_names = [i[0] for i in cursor.fetchall()]

crear_group = dbc.InputGroup(
        [
            dbc.InputGroupText("Values ("),
            dbc.Input(id='input', type='text', placeholder="ej: 'Paula', 'Jurado', 40.2"),
            dbc.InputGroupText(")"),
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
        ],
        style= {'marginTop':'1vh'}),
    html.Div(id='tabla', className='mt-4'),
    html.Div(crear_group),
    html.Br(),
    html.Div(dbc.Button("Execute", id='boton', n_clicks=0), style={"display":"flex", "justifyContent":"center"})
]),

@app.callback(Output('tabla', 'children'),
              [State('input','value'),
               Input('tabla-dropdown', 'value'),
               Input('boton','n_clicks')])
def crear_tabla(values, tabla, n):
    dic = {"billete":"Billete","cuentavirtual":"CuentaVirtual"}
    if(values is not None):
        if tabla in dic.keys():
            try:
                cursor.execute(f"CALL añadirRegistro{dic[tabla]}({values})")
            except Exception as e:
                return html.Div(html.P(f"Error en la función actualizar_tabla: {e}", style={"textAlign":"center","color":"red","fontWeight":"bold"}), 
                                style = {"display":"flex","justifyContent":"center"})
        else:
            try:
                cursor.execute(f"INSERT INTO {tabla} VALUES({values})")
            except Exception as e:
                return html.Div(html.P(f"Error en la función actualizar_tabla: {e}", style={"textAlign":"center","color":"red","fontWeight":"bold"}), 
                            style = {"display":"flex","justifyContent":"center"})   
    try:
        df = obtener_datos(tabla, cursor)
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
