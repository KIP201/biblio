from flask import Blueprint, render_template
from models import Livre, Membre, Emprunt, StatutEmprunt
from utils.database import db_manager

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    session = db_manager.get_session()
    stats = {
        'total_livres': session.query(Livre).count(),
        'livres_empruntes': session.query(Livre).filter_by(disponible=False).count(),
        'total_membres': session.query(Membre).count(),
        'emprunts_en_cours': session.query(Emprunt).filter_by(statut=StatutEmprunt.EN_COURS).count(),
        'emprunts_en_retard': session.query(Emprunt).filter_by(statut=StatutEmprunt.EN_RETARD).count(),
        'amendes_impayees': 0
    }
    return render_template('statistiques.html', stats=stats)
