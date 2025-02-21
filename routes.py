from flask import render_template, redirect, url_for, request, jsonify
from models import Livre, Membre, Emprunt, StatutEmprunt
from utils.database import db_manager
from datetime import datetime, timedelta

def init_routes(app):
    @app.route('/')
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

    @app.route('/livre/<int:livre_id>')
    def livre_details(livre_id):
        session = db_manager.get_session()
        livre = session.query(Livre).get(livre_id)
        membres_actifs = session.query(Membre).all()
        return render_template('livre_details.html', livre=livre, membres_actifs=membres_actifs)

    @app.route('/emprunter_livre/<int:livre_id>', methods=['POST'])
    def emprunter_livre(livre_id):
        session = db_manager.get_session()
        membre_id = request.form.get('membre_id')
        
        livre = session.query(Livre).get(livre_id)
        if not livre.disponible:
            return jsonify({'success': False, 'message': 'Livre non disponible'})
        
        # Création de l'emprunt
        emprunt = Emprunt(
            livre_id=livre_id,
            membre_id=membre_id,
            date_retour_prevue=datetime.now() + timedelta(days=14)
        )
        livre.disponible = False
        
        session.add(emprunt)
        session.commit()
        
        return redirect(url_for('livre_details', livre_id=livre_id))

    @app.route('/amendes')
    def amendes():
        session = db_manager.get_session()
        amendes = []  # À implémenter
        return render_template('amendes.html', amendes=amendes)