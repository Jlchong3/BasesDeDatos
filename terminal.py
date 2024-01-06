import pandas as pd
import mysql.connector as sql

#funciones

conn = sql.connect(
    host = "basesloteria.mysql.database.azure.com",
    user = "administrador",
    password = "@basesloteriaN",
    database = "loterianacional",
    autocommit=True
)

cursor = conn.cursor()

def inputValido(opciones):
    opcion = input("Elige una opción: ").strip()
    while opcion not in opciones:
        print("Opción no válida. Intenta nuevamente.")
        opcion = input("Elige una opción: ").strip()
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


def editarRegistro(cursor):
    # Pedir al usuario que seleccione una tabla
    numero_tabla = int(input("Ingrese el número de la tabla en la que desea editar un registro: "))

    # Obtener el nombre de la tabla seleccionada
    if 1 <= numero_tabla <= len(tablas):
        tabla_seleccionada = tablas[numero_tabla - 1]
    else:
        print("Número de tabla no válido.")
        return

    # Mostrar los registros existentes en la tabla
    imprimirTabla(cursor, tabla_seleccionada)

    # Obtener información sobre las columnas de la tabla
    cursor.execute(f"DESCRIBE {tabla_seleccionada}")
    columnas_info = cursor.fetchall()

    # Obtener los nombres de las columnas
    nombres_columnas = [columna[0] for columna in columnas_info]

    # Pedir al usuario que ingrese el valor de la clave primaria del registro a editar
    valor_clave_primaria = input(f"Ingrese el valor de la clave primaria para el registro a editar: ")

    # Verificar si el valor de la clave primaria existe en la tabla
    cursor.execute(f"SELECT COUNT(*) FROM {tabla_seleccionada} WHERE {nombres_columnas[0]} = %s", (valor_clave_primaria,))
    if cursor.fetchone()[0] == 0:
        print(f"Error: El valor {valor_clave_primaria} no existe en la tabla.")
        return

    # Mostrar las columnas disponibles y sus valores actuales
    cursor.execute(f"SELECT * FROM {tabla_seleccionada} WHERE {nombres_columnas[0]} = %s", (valor_clave_primaria,))
    registro_actual = cursor.fetchone()
    print("\nColumnas y valores actuales:")
    for columna, valor in zip(nombres_columnas, registro_actual):
        print(f"{columna}: {valor}")

    # Pedir al usuario que ingrese los nuevos valores para cada columna
    nuevos_valores = {}
    for nombre_columna in nombres_columnas[1:]:
        nuevo_valor = input(f"Ingrese el nuevo valor para la columna {nombre_columna} (o presione Enter para mantener el valor actual): ")
        nuevos_valores[nombre_columna] = nuevo_valor if nuevo_valor != "" else registro_actual[nombres_columnas.index(nombre_columna)]

    # Construir la consulta SQL para actualizar el registro
    consulta = f"UPDATE {tabla_seleccionada} SET {', '.join([f'{columna} = %s' for columna in nuevos_valores.keys()])} WHERE {nombres_columnas[0]} = %s"

    # Ejecutar la consulta SQL
    try:
        cursor.execute(consulta, list(nuevos_valores.values()) + [valor_clave_primaria])
        conn.commit()
        print("Registro editado correctamente.")
    except sql.Error as err:
        print(f"Error al editar el registro: {err}")

def EliminarRegistro(cursor):
    try: 
    # Pedir al usuario que seleccione una tabla
        numero_tabla = int(input("Ingrese el número de la tabla en la que desea borrar un registro: "))

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

        sentencia=f"DELETE from {tabla_seleccionada} WHERE "
        for PK in ObtenerPK(cursor,tabla_seleccionada):
            valor=int(input(f"Ingrese el valor de {PK}: "))
            if ObtenerPK(cursor,tabla_seleccionada).index(PK)==len(ObtenerPK(cursor,tabla_seleccionada))-1:
                sentencia+=f"{PK}={valor}"
            else:
                sentencia+=f"{PK}={valor} and "
        cursor.execute(sentencia)
        print("Registro borrado!")
    except Exception as e:
        print(f"Error al borrar, intente de nuevo {e}")


def ObtenerPK(cursor,tabla):
        try:
        # Obtiene la información sobre la clave primaria de la tabla
            cursor.execute(f"SHOW KEYS FROM {tabla} WHERE Key_name = 'PRIMARY'")
            columnas_clave_primaria = [columna[4] for columna in cursor.fetchall()]
            return columnas_clave_primaria
        
        except Exception as e:
            print(f"Error al obtener las columnas de la clave primaria: {e}")

# OPCIONES -------------------------------------------------------------
opciones = list("12345")
opcion = ""
while opcion != "5":
    print('''
Opciones:
  1. Añadir registro
  2. Borrar registro
  3. Editar registro
  4. Realizar consulta
  5. Salir
    ''')
    opcion = inputValido(opciones)
    match opcion:
        case "1":
            anadirRegistro(cursor)
        case "2":
            EliminarRegistro(cursor)
        case "3":
            editarRegistro(cursor)
        case "4":
            consultaRegistro(cursor)
        case "5":
            print("Sesión terminada con éxito.")
        case _:
            print("Opción no válida. Intente nuevamente.")

cursor.close()