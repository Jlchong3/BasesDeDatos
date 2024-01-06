import pandas as pd
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

# Conexión a la base de datos
conexion = create_connection("basesloteria.mysql.database.azure.com", "administrador", "@basesloteriaN", "loterianacional", 3306)

cursor = conexion.cursor()

def inputValido(opciones):
    opcion = input("Elige una opción: \n")
    while opcion not in opciones:
        opcion = input("Elige una opción: ")
    return opcion

def imprimirTabla(tabla):
    consulta_sql = f"SELECT * FROM {tabla}"
    print("Consulta SQL:", consulta_sql)
    
    try:
        cursor.execute(consulta_sql)
        rows = cursor.fetchall()
        columns = [i[0] for i in cursor.description]
        df = pd.DataFrame(rows, columns=columns)
        print(df.to_string(index=False))
        del df
    except mysql.connector.Error as err:
        print(f"Error durante la ejecución de la consulta: {err}")


opciones = list("123")
opcion = ""
while opcion != "3":
    print('''
Opciones:
  1. Tabla de Sucursales
  2. Tabla de Ventas
  3. Salir
    ''')
    opcion = inputValido(opciones)
    
    if opcion == "1":
        imprimirTabla("sucursal")
    elif opcion == "2":
        imprimirTabla("venta")
    elif opcion == "3":
        print("Sesión terminada con éxito.")
    else:
        print("Opción no válida. Inténtalo de nuevo.")

conexion.close()