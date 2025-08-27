from flask import Blueprint, render_template, request, flash, redirect
from flask_login import login_required, current_user
from models.historial_compras import agregar_historial_compra, obtener_historial_por_usuario, obtener_todos_los_historiales
from schemas.historial_compra_schema import HistorialCompraSchema
from datetime import date

historial_bp = Blueprint('historial', __name__)

# Ruta para que solo el administrador vea todas las compras
@historial_bp.route('/admin/historial')
@login_required
def ver_historial_admin():
    import json
    # Verificar si el usuario es administrador (ajusta según tu modelo de usuario)
    if not hasattr(current_user, 'is_admin') or not current_user.is_admin:
        flash('Acceso solo para administradores.', 'danger')
        return redirect('/historial')
    historial = obtener_todos_los_historiales()
    for compra in historial:
        compra['productos'] = json.loads(compra['productos'])
    return render_template('historial.html', historial=historial)

@historial_bp.route('/historial')
@login_required
def ver_historial():
    import json
    historial = obtener_historial_por_usuario(current_user.id)
    for compra in historial:
        compra['productos'] = json.loads(compra['productos'])
    return render_template('historial.html', historial=historial)

@historial_bp.route('/comprar', methods=['GET', 'POST'])
@login_required
def comprar():
    from models.carrito import obtener_carrito, vaciar_carrito
    items, total_general = obtener_carrito()
    productos = []
    for item in items:
        productos.append({
            'nombre': item[1],
            'precio': float(item[2]),
            'cantidad': int(item[3]),
            'total': float(item[4])
        })
    # Guardar historial y vaciar carrito
    import json
    agregar_historial_compra(current_user.id, date.today(), total_general, json.dumps(productos))
    vaciar_carrito()
    flash('Compra realizada y registrada en el historial.', 'success')
    return redirect('/historial')
