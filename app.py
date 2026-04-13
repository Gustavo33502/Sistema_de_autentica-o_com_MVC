from flask import Flask
from flask_mysqldb import MySQL
from config import Config

# Configuração específica da estrutura solicitada
app = Flask(
    __name__,
    template_folder='views/templates',  # Aponta para views/templates/
    static_folder='static'               # Pasta static na raiz
)
app.config.from_object(Config)

# Inicializa extensão MySQL
mysql = MySQL(app)

# Importa e registra o controller
from controllers.auth_controller import init_controller
auth_bp = init_controller(mysql)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)