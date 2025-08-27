from flask import Flask
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from models.productos import mysql
from models.usuarios import Usuario, obtener_usuario_por_id
from controllers.productos_controller import productos_bp
from controllers.usuarios_controller import usuarios_bp
from controllers.carrito_controller import carrito_bp
from controllers.historial_controller import historial_bp
from routes import bp as main_bp

# Crear la instancia de Flask
app = Flask(__name__)

# Configuración de la base de datos MySQL
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'  # Tu usuario de MySQL
app.config['MYSQL_PASSWORD'] = 'root'  # Tu contraseña de MySQL
app.config['MYSQL_DB'] = 'pfungui'  # Nombre de tu base de datos
app.config['SECRET_KEY'] = 'mysecretkey'  # Clave secreta para sesiones

# Inicializar extensiones
mysql.init_app(app)
bcrypt = Bcrypt(app)

# Configuración de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'usuarios.login'  # Ruta a la que redirigir cuando no haya sesión activa
login_manager.login_message = "Por favor, inicia sesión para acceder a esta página."

# Función para cargar un usuario basado en su ID (para Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return obtener_usuario_por_id(user_id)


app.register_blueprint(productos_bp)
app.register_blueprint(usuarios_bp)
app.register_blueprint(carrito_bp)
app.register_blueprint(historial_bp)
app.register_blueprint(main_bp)

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)