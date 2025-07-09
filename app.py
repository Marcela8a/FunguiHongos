from flask import Flask
from flask_mysqldb import MySQL
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from models import mysql, Usuario, obtener_usuario_por_id  # Importar el modelo y MySQL
from routes import bp as routes_blueprint  # Importar el Blueprint desde routes.py

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
login_manager.login_view = 'login'  # Ruta a la que redirigir cuando no haya sesión activa

# Función para cargar un usuario basado en su ID (para Flask-Login)
@login_manager.user_loader
def load_user(user_id):
    return obtener_usuario_por_id(user_id)

# Registrar el Blueprint de rutas
app.register_blueprint(routes_blueprint)

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)