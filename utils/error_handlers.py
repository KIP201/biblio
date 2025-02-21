from flask import render_template
from utils.logger import logger

def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        logger.warning(f"Page non trouvée: {error}")
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def internal_error(error):
        logger.error(f"Erreur serveur: {error}")
        return render_template('errors/500.html'), 500

    @app.errorhandler(403)
    def forbidden_error(error):
        logger.warning(f"Accès interdit: {error}")
        return render_template('errors/403.html'), 403

    @app.errorhandler(Exception)
    def unhandled_exception(e):
        logger.error(f"Erreur non gérée: {str(e)}", exc_info=True)
        return render_template('errors/500.html'), 500 