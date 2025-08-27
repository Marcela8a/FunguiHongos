

from flask_mysqldb import MySQL

mysql = MySQL()

# ----------------------
# Funciones para CARRITO
# ----------------------
def obtener_carrito():
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, precio, cantidad, total FROM carrito")
    items = cur.fetchall()
    total_general = sum(item[4] for item in items)
    cur.close()
    return items, total_general

def agregar_al_carrito(nombre, precio, cantidad):
    cur = mysql.connection.cursor()
    # Verifica si el producto ya está en el carrito por nombre
    cur.execute("SELECT cantidad FROM carrito WHERE nombre = %s", (nombre,))
    resultado = cur.fetchone()
    if resultado:
        nueva_cantidad = resultado[0] + cantidad
        total = nueva_cantidad * precio
        cur.execute("UPDATE carrito SET cantidad = %s, total = %s WHERE nombre = %s", (nueva_cantidad, total, nombre))
    else:
        total = cantidad * precio
        cur.execute("INSERT INTO carrito (nombre, precio, cantidad, total) VALUES (%s, %s, %s, %s)", (nombre, precio, cantidad, total))
    mysql.connection.commit()
    cur.close()

def eliminar_del_carrito(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM carrito WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

def vaciar_carrito():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM carrito")
    mysql.connection.commit()
    cur.close()

def vaciar_carrito_despues_de_compra():
    vaciar_carrito()
