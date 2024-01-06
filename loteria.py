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
        print("Connection to MySQL DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection


conexion = create_connection("basesloteria.mysql.database.azure.com", "administrador", "@basesloteriaN", "loterianacional", 3306) 
hola="hola"