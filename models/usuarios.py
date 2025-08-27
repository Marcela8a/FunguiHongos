from flask_mysqldb import MySQL
from flask_login import UserMixin
from flask_bcrypt import Bcrypt

mysql = MySQL()
bcrypt = Bcrypt()

class Usuario(UserMixin):
    def __init__(self, id, nombre, email, contrasena, is_admin):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.contrasena = contrasena
        self.is_admin = bool(is_admin)

# ----------------------
# Funciones para USUARIOS

# ----------------------
def obtener_usuario_por_id(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id = %s", [user_id])
    user_data = cur.fetchone()
    cur.close()
    if user_data:
        return Usuario(*user_data)
    return None

def obtener_usuario_por_email(email):
    cur = mysql.connection.cursor()
    cur.execute("SELECT id, nombre, email, contrasena, is_admin FROM usuarios WHERE email = %s", (email,))
    usuario = cur.fetchone()
    cur.close()
    if usuario:
        return Usuario(*usuario)
    return None

def registrar_usuario(nombre, email, contrasena):
    hashed_pw = bcrypt.generate_password_hash(contrasena).decode('utf-8')
    cur = mysql.connection.cursor()
    cur.execute("""
        INSERT INTO usuarios (nombre, email, contrasena, is_admin)
        VALUES (%s, %s, %s, 0)
    """, (nombre, email, hashed_pw))
    mysql.connection.commit()
    cur.close()
