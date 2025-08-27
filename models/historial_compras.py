def obtener_todos_los_historiales():
    db = MySQLdb.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        passwd=current_app.config['MYSQL_PASSWORD'],
        db=current_app.config['MYSQL_DB']
    )
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("""
        SELECT hc.*, u.nombre AS usuario_nombre, u.email AS usuario_email
        FROM historial_compras hc
        JOIN usuarios u ON hc.usuario_id = u.id
        ORDER BY hc.fecha DESC
    """)
    historial = cursor.fetchall()
    cursor.close()
    db.close()
    return historial
import MySQLdb
from flask import current_app

def agregar_historial_compra(usuario_id, fecha, total, productos):
    db = MySQLdb.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        passwd=current_app.config['MYSQL_PASSWORD'],
        db=current_app.config['MYSQL_DB']
    )
    cursor = db.cursor()
    cursor.execute("""
        INSERT INTO historial_compras (usuario_id, fecha, total, productos)
        VALUES (%s, %s, %s, %s)
    """, (usuario_id, fecha, total, str(productos)))
    db.commit()
    cursor.close()
    db.close()

def obtener_historial_por_usuario(usuario_id):
    db = MySQLdb.connect(
        host=current_app.config['MYSQL_HOST'],
        user=current_app.config['MYSQL_USER'],
        passwd=current_app.config['MYSQL_PASSWORD'],
        db=current_app.config['MYSQL_DB']
    )
    cursor = db.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("SELECT * FROM historial_compras WHERE usuario_id = %s ORDER BY fecha DESC", (usuario_id,))
    historial = cursor.fetchall()
    cursor.close()
    db.close()
    return historial
