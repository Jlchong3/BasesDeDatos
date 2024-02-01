from app import server
from app import app
from app import cursor
from pages import crear,consultar,actualizar,eliminar,home
import mysql.connector
from mysql.connector import Error

import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc


navbar = dbc.Navbar(
    html.Div([
        dbc.Container(
        [
                html.A(
                    # Use row and col to control vertical alignment of logo / brand
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src="assets/loteria-nacional-logo.png", height="100px", id='logo')),
                        ],
                        align="center",
                        justify='start',
                    ),
                    href="/home",
                ),
                
        ],
            style={"marginLeft":"2vw","width":"40%"}
        ),
        dbc.Container(
        [
            html.A(
                html.Button(
                    "Crear",
                    style={"backgroundColor":"transparent", "paddingLeft":"1.5vw","paddingRight":"1.5vw",
                           "height":"7vh","fontSize":"1.5vw","fontWeight":"600","border":"0"}
                ),
            href="/crear",
            style={"marginRight":"3vw"}
            ),

            html.A(
                html.Button(
                    "Eliminar",
                    style={"backgroundColor":"transparent", "paddingLeft":"1.5vw","paddingRight":"1.5vw",
                           "height":"7vh","fontSize":"1.5vw","fontWeight":"600","border":"0"}
                ),
            href="/eliminar",
            style={"marginRight":"3vw"}
            ),

            html.A(
                html.Button(
                    "Actualizar",
                    style={"backgroundColor":"transparent", "paddingLeft":"1.5vw","paddingRight":"1.5vw",
                           "height":"7vh","fontSize":"1.5vw","fontWeight":"600","border":"0"}
                ),
            href="/actualizar",
            style={"marginRight":"3vw"}
            ),

            html.A(
                html.Button(
                    "Consultar",
                    style={"backgroundColor":"transparent", "paddingLeft":"1.5vw","paddingRight":"1.5vw",
                           "height":"7vh","fontSize":"1.5vw","fontWeight":"600","border":"0"}
                ),
            href="/consultar",
            style={"marginRight":"1vw"}
            ),
        ],
        style={"justifyContent":"end"}
        ),
    ],
    style={"display":"flex","flex-direction":"row", "width":"100%"}),
    color="#ADD8E6",
    dark=True,
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,

    html.Div(id="page-content")
])

@app.callback(Output('page-content', 'children'),
              Input('url', 'pathname'))
def mostrar_pagina(path):
    pathname = path
    if pathname == '/crear':
        return crear.layout
    elif pathname == '/eliminar':
        return eliminar.layout
    elif pathname == '/actualizar':
        return actualizar.layout
    elif pathname == '/consultar':
        return consultar.layout
    else:
        return home.layout


if __name__ == '__main__':
    app.run_server(debug=False)

cursor.close()
conexion.close()
