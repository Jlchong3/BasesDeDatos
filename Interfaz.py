import pandas as pd
import mysql.connector as sql

#funciones

conn = sql.connect(
    host = "localhost",
    user = "root",
    password = "MARiu1234.,",
    database = "LoteriaNacional",
    autocommit=True
)

cursor = conn.cursor()

def inputValido(opciones):
    opcion = input("Eliga una opción:")
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


def anadirRegistro(cursor):
# Pedir al usuario que seleccione una tabla
    numero_tabla = int(input("Ingrese el número de la tabla en la que desea agregar un registro: "))

    # Obtener el nombre de la tabla seleccionada
    if 1 <= numero_tabla <= len(tablas):
        tabla_seleccionada = tablas[numero_tabla - 1]
    else:
        print("Número de tabla no válido.")
        return
    imprimirTabla(cursor, tabla_seleccionada)
    # Obtener información sobre las columnas de la tabla
    cursor.execute(f"DESCRIBE {tabla_seleccionada}")
    columnas_info = cursor.fetchall()

    # Obtener los nombres de las columnas
    nombres_columnas = [columna[0] for columna in columnas_info]

    # Crear un diccionario para almacenar los valores del nuevo registro
    nuevo_registro = {}

    # Pedir al usuario que ingrese los valores para cada columna
    for nombre_columna in nombres_columnas:
        valor = input(f"Ingrese el valor para la columna {nombre_columna}: ")

        # Validar si la columna es clave primaria o foránea
        if "PRI" in [tipo[3] for tipo in columnas_info if tipo[0] == nombre_columna]:
            # Verificar si el valor ya existe en la tabla (clave primaria no puede repetirse)
            cursor.execute(f"SELECT COUNT(*) FROM {tabla_seleccionada} WHERE {nombre_columna} = %s", (valor,))
            if cursor.fetchone()[0] > 0:
                print(f"Error: El valor {valor} ya existe en la columna {nombre_columna}.")
                return
            

        elif "MUL" in [tipo[3] for tipo in columnas_info if tipo[0] == nombre_columna]:


            # Verificar si el valor existe en la tabla referenciada (clave foránea)

            numero_subtabla = int(input(f"Ingrese el nombre de la tabla referenciada para la columna {nombre_columna}: "))

            # Obtener el nombre de la tabla seleccionada
            if 1 <= numero_subtabla <= len(tablas):
                tabla_subseleccionada = tablas[numero_subtabla - 1]
            else:
                print("Número de tabla no válido.")
                return

            # Obtener información sobre las columnas de la tabla
            cursor.execute(f"DESCRIBE {tabla_subseleccionada}")
            columnas_info = cursor.fetchall()

            # Construir la consulta SQL
            consulta = f"SELECT * FROM {tabla_subseleccionada} WHERE {columnas_info[0][0]} = %s"

            # Ejecutar la consulta
            cursor.execute(consulta, (valor,))

            # Obtener los resultados
            resultados = cursor.fetchall()
            if len(resultados) == 0:
                print(f"Error: El valor {valor} no existe en la tabla referenciada para la columna {nombre_columna}.")
                return

        nuevo_registro[nombre_columna] = valor

    # Construir la consulta SQL para insertar el nuevo registro
    consulta = f"INSERT INTO {tabla_seleccionada} ({', '.join(nombres_columnas)}) VALUES ({', '.join(['%s'] * len(nombres_columnas))})"

    # Ejecutar la consulta SQL
    try:
        cursor.execute(consulta, tuple(nuevo_registro.values()))
        conn.commit()
        print("Registro agregado correctamente.")
    except sql.Error as err:
        print(f"Error al agregar el registro: {err}")

def consultaRegistro(cursor):
# Pedir al usuario que seleccione una tabla
    numero_tabla = int(input("\n Ingrese el número de la tabla que desea abrir: "))

    # Verificar si el número de tabla es válido
    if 1 <= numero_tabla <= len(tablas):
        # Obtener el nombre de la tabla seleccionada
        tabla_seleccionada = tablas[numero_tabla - 1]
    else:
        print("Número de tabla no válido.")

    # Obtener información sobre las columnas de la tabla
    cursor.execute(f"DESCRIBE {tabla_seleccionada}")
    columnas_info = cursor.fetchall()

    # Mostrar al usuario las columnas disponibles
    print("\n Columnas disponibles:")
    for columna_info in columnas_info:
        print(columna_info[0])

    # Construir la consulta SQL
    consulta = f"SELECT * FROM {tabla_seleccionada} WHERE {columnas_info[0][0]} = %s"

    # Pedir al usuario que ingrese el valor de la clave primaria
    valor_clave_primaria = input(f"\n Ingrese el valor de la clave primaria para la columna {columnas_info[0][0]}: ")

    # Ejecutar la consulta
    cursor.execute(consulta, (valor_clave_primaria,))

    # Obtener los resultados
    resultados = cursor.fetchall()

    # Mostrar los resultados
    print("Resultados:")
    for resultado in resultados:
        print(resultado)

#MOSTRAR TABLAS DE LA BASE ---------------------------------------------------
cursor.execute("SHOW TABLES")
tablas = [tabla[0] for tabla in cursor]
print("\n Bienvenidos a la Base de Datos de la Loteria Nacional \n Tablas disponibles:")

for i, tabla in enumerate(tablas, start=1):
    print(f"{i}. {tabla}")

# OPCIoNES -------------------------------------------------------------
opciones = list("1234")
opcion = ""
while opcion != "4":
    print('''
Opciones:
  1. Anadir registro
  2. Borrar registro
  3. Editar registro
  4. Realizar consulta
    ''')
    opcion = inputValido(opciones)
    match opcion:
        case "1":
            anadirRegistro(cursor)
        case "2":
            consultaRegistro(cursor)
        case "3":
            print("Editar ") 
        case "4":
            consultaRegistro(cursor)
        case _:
            print("Sesión terminada con exito.")   




opciones = list("123")
opcion = ""
while opcion != "3":
    print('''
Opciones:
  1. Tabla de Sucursales
  2. Table de Ventas
  3. salir
    ''')
    opcion = inputValido(opciones)
    match opcion:
        case "1":
            imprimirTabla(cursor, "sucursal")
        case "2":
            imprimirTabla(cursor, "venta")
        case _:
            print("Sesión terminada con exito.")

cursor.close()