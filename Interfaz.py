import pandas as pd
import mysql.connector as sql

#funciones

def inputValido(opciones):
    opcion = input("Eliga una opción: \n")
    while opcion not in opciones:
        opcion = input("Eliga una opción: ")
    return opcion

def imprimirTabla(cursor, tabla):
    cursor.execute(f"Select * from {tabla}")
    rows = cursor.fetchall()
    columns = [i[0] for i in cursor.description]
    df = pd.DataFrame(rows, columns=columns)
    print(df.to_string(index=False))
    del df

conn = sql.connect(
    host = "localhost",
    user = "root",
    password = "",
    database = ""
)

cursor = conn.cursor()

opciones = list("123")
opcion = ""
while opcion != "3":
    print('''
Opciones:
  1. Tabla de Ganadores
  2. Table de Sorteos
  3. salir
    ''')
    opcion = inputValido(opciones)
    match opcion:
        case "1":
            imprimirTabla(cursor, "ganador")
        case "2":
            imprimirTabla(cursor, "sorteo")
        case _:
            print("Sesión terminada con exito.")

