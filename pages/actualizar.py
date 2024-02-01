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

update_group = dbc.InputGroup(
        [
            dbc.InputGroupText("NEW Values ("),
            dbc.Input(id='input-update', type='text', placeholder="ej: 0193234940,'Paula', 'Jurado', 40.2"),
            dbc.InputGroupText(")"),
        ]
    )
index_group = dbc.InputGroup(
        [
            dbc.InputGroupText("INDEX"),
            dbc.Input(id='input-index', type='text', placeholder="ej: 13"),
        ]
    )

layout = dbc.Container([
    html.Div([
        dcc.Dropdown(
            id='tabla-dropdown',
            options=[{'label': f'Tabla de {table}', 'value': table} for table in table_names],
            value= table_names[1],
            className='form-control',
        ),
        ],
        style= {'marginTop':'1vh'}),
    html.Div(id='tabla-update', className='mt-4'),
    html.Div(update_group),
    html.Div(id = "index"),
    html.Br(),
    html.Div(dbc.Button("Execute", id='boton', n_clicks=0), style={"display":"flex", "justifyContent":"center"})
]),

@app.callback(Output('index', 'children'),
              [Input('tabla-dropdown', 'value'),])
def aparecerOpcion(tabla):
    dic = {"billete":"Billete","cuentavirtual":"CuentaVirtual"}
    if tabla not in dic.keys():
        return index_group

@app.callback(Output('tabla-update', 'children'),
              [State('input-update','value'),
               State('input-index', 'value'),
               Input('tabla-dropdown', 'value'),
               Input('boton','n_clicks')])
def update_tabla(values, id , tabla, n):
    dic = {"billete":"Billete","cuentavirtual":"CuentaVirtual"}
    if(values is not None):
        if tabla in dic.keys():
            try:
                cursor.execute(f"CALL editarRegistro{dic[tabla]}({values})")
            except Exception as e:
                return html.Div(html.P(f"Error en la función actualizar_tabla: {e}", style={"textAlign":"center","color":"red","fontWeight":"bold"}), 
                                style = {"display":"flex","justifyContent":"center"})
        elif id is not None:
            try:
                sets = ""
                cursor.execute(f"DESCRIBE {tabla}")
                columns = [column[0] for column in cursor.fetchall()]
                values = values.split(",")
                for column, value in zip(columns[1:],values):
                    if column == columns[1]:
                        sets += f"{column} = {value}"
                        continue
                    sets += f",{column} = {value}"
                print(sets)
                cursor.execute(f"Update {tabla} SET {sets} WHERE {columns[0]} = {id}")
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
