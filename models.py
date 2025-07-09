from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

# Inicialización de MySQL
mysql = MySQL()
bcrypt = Bcrypt()

# ----------------------
# Funciones para PRODUCTOS
# ----------------------

def obtener_productos():
    """Obtiene todos los productos disponibles."""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos WHERE disponible = 1")
    productos = cur.fetchall()
    cur.close()
    return productos

def obtener_producto_por_id(id):
    """Obtiene un producto por su ID."""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos WHERE id = %s", (id,))
    productos = cur.fetchone()
    cur.close()
    return productos


def agregar_producto(nombre, descripcion, precio, stock, activo, disponible):
    """Agrega un nuevo producto a la base de datos."""
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO productos (nombre, descripcion, precio, stock, activo, disponible)
        VALUES (%s, %s, %s, %s, %s, %s)
    """, (nombre, descripcion, precio, stock, activo, disponible))
    mysql.connection.commit()
    cur.close()

def actualizar_producto(id, nombre, descripcion, precio, stock, activo, disponible):
    """Actualiza un producto existente."""
    cur = mysql.connection.cursor()
    cur.execute("""
        UPDATE productos
        SET nombre = %s, descripcion = %s, precio = %s, stock = %s, activo = %s, disponible = %s
        WHERE id = %s
    """, (nombre, descripcion, precio, stock, activo, disponible, id))
    mysql.connection.commit()
    cur.close()

def eliminar_producto_por_id(id):
    """Elimina un producto por su ID."""
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM productos WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

# ----------------------
# Funciones para USUARIOS
# ----------------------

class Usuario(UserMixin):
    """Clase que representa un usuario, compatible con Flask-Login."""
    def __init__(self, id, nombre, email, contrasena, is_admin):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.contrasena = contrasena
        self.is_admin = is_admin

def obtener_usuario_por_id(user_id):
    """Obtiene un usuario por su ID."""
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id = %s", [user_id])
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        return Usuario(id=user_data[0], nombre=user_data[1], email=user_data[2], contrasena=user_data[3], is_admin=user_data[4])
    return None

def obtener_usuario_por_email(email):
    """Obtiene un usuario por su correo electrónico."""
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, email, contrasena, is_admin FROM usuarios WHERE email = %s", (email,))
    usuario = cur.fetchone()
    cur.close()
    if usuario:
        return Usuario(id=usuario[0], nombre=usuario[1], email=usuario[2], contrasena=usuario[3], is_admin=usuario[4])
    return None

def registrar_usuario(nombre, email, contrasena):
    """Registra un nuevo usuario."""
    hashed_pw = bcrypt.generate_password_hash(contrasena).decode('utf-8') 
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO usuarios (nombre, email, contrasena)
        VALUES (%s, %s, %s)
    """, (nombre, email, hashed_pw))
    mysql.connection.commit()
    cur.close()

# ----------------------
# Funciones para CARRITO
# ----------------------

def obtener_carrito():
    """Obtiene los productos del carrito actual y calcula el total general."""
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT carrito.id, productos.nombre, productos.precio, carrito.cantidad,
               productos.precio * carrito.cantidad AS total
        FROM carrito
        JOIN productos ON carrito.id = productos.id
    """)
    items = cur.fetchall()
    cur.close()
    total_general = sum(item[4] for item in items)  # Total general
    return items, total_general

def agregar_al_carrito(producto_id, cantidad):
    """Agrega un producto al carrito."""
    cur = mysql.connection.cursor()
    cur.execute("INSERT INTO carrito (id, cantidad) VALUES (%s, %s)", (producto_id, cantidad))
    mysql.connection.commit()
    cur.close()

def eliminar_del_carrito(producto_id):
    """Elimina un producto del carrito."""
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM carrito WHERE id = %s", (producto_id,))
    mysql.connection.commit()
    cur.close()

def vaciar_carrito():
    """Vacía todo el carrito."""
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM carrito")
    mysql.connection.commit()
    cur.close()

def  vaciar_carrito_despues_de_compra():
    """Finaliza la compra y vacía el carrito."""
    
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM carrito")  # Vaciar el carrito después de la compra
    mysql.connection.commit()
    cur.close()

# ----------------------
# Funciones para CHECKOUT
# ----------------------

def obtener_checkout():
    """Obtiene la información del carrito para el checkout."""
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT carrito.id, productos.nombre, productos.precio, carrito.cantidad,
               productos.precio * carrito.cantidad AS total
        FROM carrito
        JOIN productos ON carrito.id = productos.id
    """)
    items = cur.fetchall()
    cur.close()
    total_general = sum(item[4] for item in items)
    return items, total_general