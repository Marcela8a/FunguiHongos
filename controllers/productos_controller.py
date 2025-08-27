from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from models.productos import obtener_productos, obtener_producto_por_id, agregar_producto, actualizar_producto, eliminar_producto_por_id
 # ProductoSchema eliminado, no se usa

productos_bp = Blueprint('productos', __name__)
# Ruta raíz para el logo y acceso directo al home
@productos_bp.route('/')
def bienvenida():
    return redirect(url_for('productos.home'))

@productos_bp.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@productos_bp.route('/contacto')
def contacto():
    return render_template('contacto.html')

@productos_bp.route('/recetas')
def recetas():
    return render_template('recetas.html')

@productos_bp.route('/home')
def home():
    productos = obtener_productos()
    return render_template('home.html', productos=productos)

@productos_bp.route('/productos/<int:id>')
def producto_details(id):
    producto = obtener_producto_por_id(id)
    return render_template('producto_details.html', productos=producto)

@productos_bp.route('/productos/crear', methods=['GET', 'POST'])
@login_required
def crear_producto():
    if request.method == 'POST':
        data = {
            'nombre': request.form['nombre'],
            'descripcion': request.form['descripcion'],
            'precio': float(request.form['precio']),
            'stock': int(request.form['stock']),
            'imagen': request.form.get('imagen', '')
        }
        activo = 1 if 'activo' in request.form else 0
        disponible = 1 if 'disponible' in request.form else 0
        agregar_producto(data['nombre'], data['descripcion'], data['precio'], data['stock'], activo, disponible)
        flash('Producto creado correctamente.', 'success')
        return redirect(url_for('productos.home'))
    return render_template('crear_producto.html')

@productos_bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    producto = obtener_producto_por_id(id)
    if request.method == 'POST':
        data = {
            'nombre': request.form['nombre'],
            'descripcion': request.form['descripcion'],
            'precio': float(request.form['precio']),
            'stock': int(request.form['stock']),
            'imagen': request.form.get('imagen', '')
        }
        activo = request.form['activo']
        disponible = request.form['disponible']
        actualizar_producto(id, data['nombre'], data['descripcion'], data['precio'], data['stock'], activo, disponible)
        flash('Producto actualizado correctamente.', 'success')
        return redirect(url_for('productos.home'))
    return render_template('editar_producto.html', producto=producto)

@productos_bp.route('/productos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    eliminar_producto_por_id(id)
    flash('Producto eliminado correctamente.', 'success')
    return redirect(url_for('productos.home'))
