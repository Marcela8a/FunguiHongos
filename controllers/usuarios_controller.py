from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from models.usuarios import obtener_usuario_por_email, registrar_usuario
from flask_bcrypt import check_password_hash

usuarios_bp = Blueprint('usuarios', __name__)

@usuarios_bp.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contrasena = request.form['contrasena']
        registrar_usuario(nombre, email, contrasena)
        flash('Usuario registrado exitosamente.', 'success')
        return redirect(url_for('usuarios.login'))
    return render_template('registro.html')

@usuarios_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contrasena = request.form['contrasena']
        usuario = obtener_usuario_por_email(email)
        if usuario and usuario.contrasena and check_password_hash(usuario.contrasena, contrasena):
            login_user(usuario)
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('productos.home'))
        else:
            flash('Credenciales incorrectas.', 'danger')
    return render_template('login.html')

@usuarios_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('productos.home'))
