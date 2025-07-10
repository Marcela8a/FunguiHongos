from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bcrypt import Bcrypt
from datetime import datetime

# Importa las funciones del modelo (por ejemplo, para interactuar con la base de datos)
from models import obtener_productos, obtener_producto_por_id, registrar_usuario, obtener_usuario_por_email, agregar_producto, actualizar_producto, eliminar_producto_por_id, obtener_carrito, agregar_al_carrito, eliminar_del_carrito, vaciar_carrito,  vaciar_carrito_despues_de_compra

# Crear un Blueprint para las rutas
bp = Blueprint('', __name__)
bcrypt = Bcrypt()

@bp.route('/')
def bienvenida():
    return render_template('bienvenida.html')


@bp.route('/home')
def home():
    productos = obtener_productos()
    return render_template('home.html', productos=productos)

@bp.route('/nosotros')
def nosotros():
    return render_template('nosotros.html')

@bp.route('/contacto')
def contacto():
    return render_template('contacto.html')

@bp.route('/recetas')
def recetas():
    return render_template('recetas.html')

@bp.route('/productos/<int:id>')
def producto_details(id):
    productos = obtener_producto_por_id(id)
    return render_template('producto_details.html', productos=productos
)

@bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contrasena = request.form['contrasena']

        # Verificar si el correo ya existe
        usuario = obtener_usuario_por_email(email)
        if usuario:
            flash('Este correo ya está registrado. Por favor inicia sesión.', 'warning')
            return redirect(url_for('registro'))

        # Registrar usuario en la base de datos
        registrar_usuario(nombre, email, contrasena)
        flash('Usuario registrado exitosamente. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contrasena = request.form['contrasena']

        # Verificar usuario
        usuario = obtener_usuario_por_email(email)
        if usuario and bcrypt.check_password_hash(usuario.contrasena, contrasena):
            login_user(usuario)
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('home'))
        else:
            flash('Credenciales incorrectas.', 'danger')

    return render_template('login.html')

@bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('home'))

@bp.route('/productos/crear', methods=['GET', 'POST'])
@login_required
def crear_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        activo = 1 if request.form.get('activo') == 'on' else 0
        disponible = 1 if request.form.get('disponible') == 'on' else 0

        agregar_producto(nombre, descripcion, precio, stock, activo, disponible)
        flash('Producto registrado exitosamente!', 'success')
        return redirect(url_for('home'))

    return render_template('crear_producto.html')

@bp.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    
    producto = obtener_producto_por_id(id)
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']
        activo = request.form['activo']
        disponible = request.form['disponible']

        actualizar_producto(id, nombre, descripcion, precio, stock, activo, disponible)
        flash('Producto actualizado correctamente.', 'success')
        return redirect(url_for('producto_details', id=id))

    return render_template('editar_producto.html', producto=producto)

@bp.route('/productos/eliminar/<int:id>', methods=['POST'])
@login_required
def eliminar_producto(id):
    eliminar_producto_por_id(id)
    flash('Producto eliminado correctamente.', 'success')
    return redirect(url_for('home'))

@bp.route('/carrito')
@login_required
def carrito():
    items, total_general = obtener_carrito()
    return render_template('cart.html', items=items, total_general=total_general)

@bp.route('/agregar_carrito/<int:id>', methods=['POST'])
@login_required
def agregar_carrito(id):
    cantidad = int(request.form['cantidad'])
    agregar_al_carrito(id, cantidad)
    flash('Producto agregado al carrito!', 'success')
    return redirect(url_for('carrito'))

@bp.route('/quitar_del_carrito/<int:id>', methods=['POST'])
@login_required
def quitar_del_carrito(id):
    eliminar_del_carrito(id)
    flash('Producto eliminado del carrito.', 'info')
    return redirect(url_for('carrito'))

@bp.route('/vaciar_carrito', methods=['POST'])
@login_required
def vaciar_carrito():
    vaciar_carrito()
    flash('Carrito vaciado exitosamente.', 'info')
    return redirect(url_for('carrito'))

@bp.route('/checkout')
@login_required
def checkout():
    items, total_general = obtener_carrito()
    return render_template('checkout.html', items=items, total_general=total_general)

@bp.route('/finalizar_compra')
@login_required
def finalizar_compra():
      
    flash('Compra finalizada con éxito.', 'success')
    vaciar_carrito_despues_de_compra() 
    return redirect(url_for('home'))