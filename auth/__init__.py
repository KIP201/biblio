from flask import Flask
from .auth import login_required, has_role
from .routes import auth_bp

def init_auth(app: Flask):
    """Initialise le système d'authentification"""
    app.register_blueprint(auth_bp)
    
    # Ajout des décorateurs à l'application
    app.login_required = login_required
    app.has_role = has_role
    
    # Configuration de la session
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['PERMANENT_SESSION_LIFETIME'] = app.config.get('PERMANENT_SESSION_LIFETIME', 86400)  # 24h par défaut
    
    return app 