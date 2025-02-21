from flask import Blueprint
from .livres import livres_bp
from .amendes import amendes_bp

def init_routes(app):
    app.register_blueprint(livres_bp)
    app.register_blueprint(amendes_bp) 