import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import mysql.connector
from mysql.connector import Error
from app import app
from app import cursor

layout = dbc.Container([
    html.Div([
        dbc.Carousel(
            items=[
                {'key':'1','src':'/assets/carusel1.jpeg'},
                {'key':'2','src':'/assets/carusel2.jpeg'},
                {'key':'3','src':'/assets/carusel3.jpeg'},
                {'key':'4','src':'/assets/carusel4.jpeg'},
                {'key':'5','src':'/assets/carusel5.jpeg'},
                ],
                controls=True,
                interval=3000,
                indicators = False,
                style = {'width':'46vw'}
                ),
        html.Div(html.Img(alt = 'publicidad', src = 'assets/publicidad.jpeg', style = {"width":"24.15vw", "marginLeft":"1vw"}))
    ], style = {"marginTop": "8vh", "display":"flex", "flexDirection":"row"})],
    style = {"display":"flex","justifyContent":"center"})


