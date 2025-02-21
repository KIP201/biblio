from flask import Flask
from flask_login import LoginManager
from models import User
from utils.database import db_manager
from routes import init_routes
from config import config
from config.logging import setup_logging

app = Flask(__name__)
app.config.from_object(config)

# Configuration de Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    session = db_manager.get_session()
    return session.query(User).get(int(user_id))

# Initialisation des routes
init_routes(app)

# Configuration des logs
setup_logging(app)

if __name__ == '__main__':
    # Initialisation de la base de données
    db_manager.init_db()
    app.run(debug=config.DEBUG)