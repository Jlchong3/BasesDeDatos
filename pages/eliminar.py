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

delete_group = dbc.InputGroup(
        [
            dbc.InputGroupText("INDEX"),
            dbc.Input(id='input-delete', type='text', placeholder="ej: 13"),
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
    html.Div(id='tabla-delete', className='mt-4'),
    html.Div(delete_group),
    html.Br(),
    html.Div(dbc.Button("Execute", id='boton', n_clicks=0), style={"display":"flex", "justifyContent":"center"})
]),

@app.callback(Output('tabla-delete', 'children'),
              [State('input-delete','value'),
               Input('tabla-dropdown', 'value'),
               Input('boton','n_clicks')])
def delete_tabla(index, tabla, n):
    dic = {"billete":"Billete","cuentavirtual":"CuentaVirtual"}
    if(index is not None):
        if tabla in dic.keys():
            try:
                cursor.execute(f"CALL eliminarRegistro{dic[tabla]}({index})")
            except Exception as e:
                return html.Div(html.P(f"Error en la función actualizar_tabla: {e}", style={"textAlign":"center","color":"red","fontWeight":"bold"}), 
                                style = {"display":"flex","justifyContent":"center"})
        else:
            try:
                cursor.execute(f"DESCRIBE {tabla}")
                columns = [column[0] for column in cursor.fetchall()]
                cursor.execute(f"DELETE FROM {tabla} WHERE {columns[0]} = {index}")
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
