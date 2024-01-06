from app import server
from app import app

import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import mysql.connector
from mysql.connector import Error

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

conexion = create_connection("basesloteria.mysql.database.azure.com", "administrador", "@basesloteriaN", "loterianacional", 3306)

navbar = dbc.Navbar(
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
        style={"marginLeft":"2vw"}


        ),
    color="#ADD8E6",
    dark=True,
)

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
])

if __name__ == '__main__':
    app.run_server(debug=True)

conexion.close()
