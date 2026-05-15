from flask import Blueprint, render_template
from models import Membre
from utils.database import db_manager

membres_bp = Blueprint('membres', __name__)

@membres_bp.route('/membres')
def liste_membres():
    session = db_manager.get_session()
    membres = session.query(Membre).all()
    return render_template('base.html') # Placeholder template or create a new one
