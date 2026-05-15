from flask import Blueprint
from .livres import livres_bp
from .amendes import amendes_bp
from .main import main_bp
from .membres import membres_bp

def init_routes(app):
    app.register_blueprint(main_bp)
    app.register_blueprint(livres_bp)
    app.register_blueprint(amendes_bp)
    app.register_blueprint(membres_bp)
