import pandas as pd
import mysql.connector as sql

#funciones




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
    numero_tabla = int(input("\n Ingrese el número de la tabla que desea abrir: \n"))

    # Verificar si el número de tabla es válido
    if 1 <= numero_tabla <= len(tablas):
        # Obtener el nombre de la tabla seleccionada
        tabla_seleccionada = tablas[numero_tabla - 1]

        # Mostrar información de la tabla seleccionada
        print(f"Abriendo la tabla: {tabla_seleccionada}")
        imprimirTabla(cursor, f"{tabla_seleccionada}")

    else:
        print("Número de tabla no válido.")

    #MOSTRAR COLUMNAS Y CLAVES PRIMARIAS O FORANEAS 
    consulta_ultimo_valor = f"SELECT MAX(col1) FROM {tabla_seleccionada}"
    cursor.execute(consulta_ultimo_valor)
    ultimo_valor_primaria = cursor.fetchone()[0]

    # Verificar si hay algún valor previo y asignar el nuevo valor
    nuevo_valor_primaria = 1 if ultimo_valor_primaria is None else ultimo_valor_primaria + 1

    # Verificar la existencia de la clave foránea en su respectiva tabla
    consulta_verificar_foranea = f"SELECT * FROM tabla_foranea WHERE col_foranea = {col2}"
    cursor.execute(consulta_verificar_foranea)
    if cursor.fetchone() is None:
        raise ValueError("La clave foránea no existe en la tabla_foranea.")
    
    # Consulta SQL para insertar el nuevo registro
    consulta_insertar = f"INSERT INTO {tabla_seleccionada} (col1, col2, col3, col4) VALUES (%s, %s, %s, %s)"

    # Datos para insertar
    datos_insertar = (nuevo_valor_primaria, col2, col3, col4)

    # Ejecutar la consulta SQL para insertar el nuevo registro
    cursor.execute(consulta_insertar, datos_insertar)

    conn.commit()

    del df

def consultaRegistro(cursor):
    # Pedir al usuario que seleccione una tabla
    numero_tabla = int(input("\n Ingrese el número de la tabla que desea abrir: \n"))

    # Verificar si el número de tabla es válido
    if 1 <= numero_tabla <= len(tablas):
        # Obtener el nombre de la tabla seleccionada
        tabla_seleccionada = tablas[numero_tabla - 1]

        # Mostrar información de la tabla seleccionada
        print(f"Abriendo la tabla: {tabla_seleccionada}")
        imprimirTabla(cursor, f"{tabla_seleccionada}")

    else:
        print("Número de tabla no válido.")

        # Obtén la información de la tabla para determinar la columna de la clave primaria
        cursor.execute(f"DESCRIBE numero_tabla")
        filas = cursor.fetchall()
        columna_clave_primaria = 0

        for fila in filas:
            if 'PRI' in fila:
                columna_clave_primaria = fila[0]
                break

        if columna_clave_primaria is None:
            raise ValueError("No se encontró una columna de clave primaria en la tabla.")

        # Construye la consulta SQL utilizando la columna de la clave primaria
        consulta = f"SELECT * FROM {tabla} WHERE {columna_clave_primaria} = %s"

        # Ejecuta la consulta
        cursor.execute(consulta, (clave_primaria_valor,))

        resultado = cursor.fetchone()
        print(resultado)


        del df

conn = sql.connect(
    host = "localhost",
    user = "root",
    password = "MARiu1234.,",
    database = "LoteriaNacional"
)

cursor = conn.cursor()




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

