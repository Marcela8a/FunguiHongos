from flask_mysqldb import MySQL

mysql = MySQL()

# ----------------------
# Funciones para PRODUCTOS
# ----------------------
def obtener_productos():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos WHERE disponible = 1")
    productos = cur.fetchall()
    cur.close()
    return productos

def obtener_producto_por_id(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos WHERE id = %s", (id,))
    producto = cur.fetchone()
    cur.close()
    return producto

def agregar_producto(nombre, descripcion, precio, stock, activo, disponible):
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO productos (nombre, descripcion, precio, stock, activo, disponible)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nombre, descripcion, precio, stock, activo, disponible))
    mysql.connection.commit()
    cur.close()

def actualizar_producto(id, nombre, descripcion, precio, stock, activo, disponible):
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE productos
        SET nombre = %s, descripcion = %s, precio = %s, stock = %s, activo = %s, disponible = %s
        WHERE id = %s
    """, (nombre, descripcion, precio, stock, activo, disponible, id))
    mysql.connection.commit()
    cur.close()

def eliminar_producto_por_id(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM productos WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
