from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.carrito import obtener_carrito, agregar_al_carrito, eliminar_del_carrito, vaciar_carrito, vaciar_carrito_despues_de_compra
from models.productos import obtener_producto_por_id

carrito_bp = Blueprint('carrito', __name__)

@carrito_bp.route('/carrito')
@login_required
def carrito():
    items, total_general = obtener_carrito()
    return render_template('cart.html', items=items, total_general=total_general)

@carrito_bp.route('/agregar_carrito/<int:id>', methods=['POST'])
@login_required
def agregar_carrito(id):
    cantidad = int(request.form['cantidad'])
    producto = obtener_producto_por_id(id)
    nombre = producto[1]
    precio = producto[3]
    agregar_al_carrito(nombre, precio, cantidad)
    flash('Producto agregado al carrito!', 'success')
    return redirect(url_for('carrito.carrito'))

@carrito_bp.route('/quitar_del_carrito/<int:id>', methods=['POST'])
@login_required
def quitar_del_carrito(id):
    eliminar_del_carrito(id)
    flash('Producto eliminado del carrito.', 'success')
    return redirect(url_for('carrito.carrito'))

@carrito_bp.route('/vaciar_carrito', methods=['POST'])
@login_required
def vaciar_carrito_view():
    vaciar_carrito()
    flash('Carrito vaciado correctamente.', 'success')
    return redirect(url_for('carrito.carrito'))

@carrito_bp.route('/checkout')
@login_required
def checkout():
    items, total_general = obtener_carrito()
    return render_template('checkout.html', items=items, total_general=total_general)


@carrito_bp.route('/finalizar_compra')
@login_required
def finalizar_compra():
    # Redirigir al endpoint que guarda el historial y vacía el carrito
    return redirect('/comprar')
