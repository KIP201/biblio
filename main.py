from flask import Flask
from utils.database import db_manager
from utils.scheduler import scheduler
from utils.error_handlers import register_error_handlers
from routes import init_routes
from config.logging_config import setup_logging
from config.app_config import Config
from auth import init_auth

def create_app():
    # Configuration du logging
    setup_logging()
    
    # Création de l'application
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialisation de la base de données
    if not db_manager.init_db():
        raise RuntimeError("Impossible d'initialiser la base de données")
    
    # Initialisation du planificateur
    scheduler.start()
    
    # Enregistrement des routes
    init_routes(app)
    
    # Enregistrement de l'authentification
    init_auth(app)
    
    # Enregistrement des gestionnaires d'erreurs
    register_error_handlers(app)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='localhost', port=5000, debug=False) 