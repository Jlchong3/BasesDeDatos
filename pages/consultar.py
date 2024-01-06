import pandas as pd
import dash
from dash import dcc, html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc
import mysql.connector
from mysql.connector import Error
from app import app
from app import cursor

layout = dbc.Container(html.P("hola"))
