import dash
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

cursor = conexion.cursor()

app = dash.Dash(__name__, external_stylesheets=['https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css'])

server = app.server
app.config.suppress_callback_exceptions = True

