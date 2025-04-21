from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt


app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'  # Tu usuario de MySQL
app.config['MYSQL_PASSWORD'] = 'root'  # Tu contraseña de MySQL
app.config['MYSQL_DB'] = 'pfungui'  # Nombre de tu base de datos
app.config['SECRET_KEY'] = 'mysecretkey'

mysql = MySQL(app)
bcrypt = Bcrypt(app)

@app.route('/')
def home():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos WHERE disponible = 1")
    productos = cur.fetchall()
    print(str(productos))
    cur.close()
    return render_template('home.html', productos=productos)

@app.route('/productos/<int:id>')
def producto_details(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos WHERE id = %s", (id,))
    productos = cur.fetchone()
    cur.close()
    return render_template('producto_details.html', productos=productos)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Redirigir a login si no está autenticado

# Crear la clase Usuario que implementa UserMixin
class Usuario(UserMixin):
    def __init__(self, id, nombre, email, contrasena, is_admin):
        self.id = id
        self.nombre = nombre
        self.email = email
        self.contrasena = contrasena
        self.is_admin = is_admin 

# Función para cargar el usuario
@login_manager.user_loader
def load_user(user_id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM usuarios WHERE id = %s", [user_id])
    user_data = cur.fetchone()
    if user_data:
        return Usuario(id=user_data[0], nombre=user_data[1], email=user_data[2], contrasena=user_data[3], is_admin=user_data[4])
    return None

@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        contrasena = request.form['contrasena']

        # Verificar si el correo ya existe
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM usuarios WHERE email = %s", (email,))
        usuario = cur.fetchone()

        if usuario:
            flash('Este correo ya está registrado. Por favor inicia sesión.', 'warning')
            cur.close()
            return redirect(url_for('registro'))

        # Hashear la contraseña antes de guardarla
        hashed_pw = bcrypt.generate_password_hash(contrasena).decode('utf-8')

        # Insertar nuevo usuario
        cur.execute(
            "INSERT INTO usuarios (nombre, email, contrasena) VALUES (%s, %s, %s)",
            (nombre, email, hashed_pw)
        )
        mysql.connection.commit()
        cur.close()

        flash('Usuario registrado exitosamente. Ahora puedes iniciar sesión.', 'success')

    return render_template('registro.html')



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        contrasena = request.form['contrasena']

        cur = mysql.connection.cursor()
      
       
       # Assuming cur is a cursor object
        cur.execute('SELECT id, nombre, email, contrasena, is_admin FROM usuarios WHERE email = %s', (email,))
        usuario = cur.fetchone()  # Fetch the result
        print(str(usuario))

        if usuario and bcrypt.check_password_hash(usuario[3], contrasena):  # Compara la contraseña
            user = Usuario(id=usuario[0], nombre=usuario[1], email=usuario[2], contrasena=usuario[3], is_admin=usuario[4])
            login_user(user)
            flash('Inicio de sesión exitoso.', 'success')
            return redirect(url_for('home'))  # Redirige al home después del login
        else:
            flash('Credenciales incorrectas.', 'danger')

        cur.close()

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión exitosamente.', 'info')
    return redirect(url_for('home'))


@app.route('/agregar_carrito/<int:id>', methods=['POST'])
@login_required
def agregar_carrito(id):
    cantidad = int(request.form['cantidad'])
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos WHERE id = %s", (id,))
    productos = cur.fetchone()

    if productos:      
        cur.execute("INSERT INTO carrito (id, cantidad) VALUES (%s, %s)", (productos[0], cantidad))
        mysql.connection.commit()
        flash('Producto agregado al carrito!', 'success')
    
    cur.close()
    return redirect(url_for('carrito'))

@app.route('/productos/crear', methods=['GET', 'POST'])
@login_required
def crear_producto():
    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = float(request.form['precio'])
        stock = int(request.form['stock'])
        activo = 1 if request.form.get('activo') == 'on' else 0
        disponible = 1 if request.form.get('disponible') == 'on' else 0

        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO productos (nombre, descripcion, precio, stock, activo, disponible)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (nombre, descripcion, precio, stock, activo, disponible))
        mysql.connection.commit()
        cur.close()

        flash('Producto registrado exitosamente!', 'success')
        return redirect(url_for('home'))

    return render_template('crear_producto.html')

@app.route('/productos/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def editar_producto(id):
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM productos WHERE id = %s", (id,))
    producto = cur.fetchone()

    if request.method == 'POST':
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        precio = request.form['precio']
        stock = request.form['stock']
        activo = request.form['activo']
        disponible = request.form['disponible']

        cur.execute("""
            UPDATE productos
            SET nombre = %s, descripcion = %s, precio = %s, stock = %s, activo = %s, disponible = %s
            WHERE id = %s
        """, (nombre, descripcion, precio, stock, activo, disponible, id))
        mysql.connection.commit()
        cur.close()

        flash('Producto actualizado correctamente', 'success')
        return redirect(url_for('producto_details', id=id))

    cur.close()
    return render_template('editar_producto.html', producto=producto)

@app.route('/productos/eliminar/<int:id>', methods=['GET', 'POST'])
@login_required
def eliminar_producto(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM productos WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()

    flash('Producto eliminado correctamente', 'success')
    return redirect(url_for('home'))

@app.route('/carrito')
@login_required
def carrito():
    cur = mysql.connection.cursor()
    cur.execute("""
        SELECT carrito.id, productos.nombre, productos.precio, carrito.cantidad, 
               productos.precio * carrito.cantidad AS total
        FROM carrito
        JOIN productos ON carrito.id = productos.id
    """)
    items = cur.fetchall()
    cur.close()

    total_general = sum(item[4] for item in items)  # suma de los totales por producto

    return render_template('cart.html', items=items, total_general=total_general)


@app.route('/quitar_del_carrito/<int:id>', methods=['POST'])
@login_required
def quitar_del_carrito(id):
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM carrito WHERE id = %s", (id,))
    mysql.connection.commit()
    cur.close()
    flash('Producto eliminado del carrito', 'info')
    return redirect(url_for('carrito'))

@app.route('/vaciar_carrito', methods=['POST'])
@login_required
def vaciar_carrito():
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM carrito")
    mysql.connection.commit()
    cur.close()
    flash('Carrito vaciado exitosamente', 'info')
    return redirect(url_for('carrito'))

@app.route('/checkout')
@login_required
def checkout():
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

    # Aquí agregarías el procesamiento de la compra, por ejemplo, detalles de pago, etc.

    return render_template('checkout.html', items=items, total_general=total_general)


@app.route('/finalizar_compra')
@login_required
def finalizar_compra():
    # Aquí puedes agregar la lógica para crear un pedido, cobrarlo, etc.
    flash('Compra finalizada con éxito', 'success')

    # Después de la compra, puedes vaciar el carrito y redirigir a una página de confirmación
    cur = mysql.connection.cursor()
    cur.execute("DELETE FROM carrito")  # Vaciar carrito
    mysql.connection.commit()
    cur.close()

    return redirect(url_for('home'))  # Redirigir al inicio después de finalizar la compra


if __name__ == '__main__':
    app.run(debug=True)
