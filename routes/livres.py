from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from models import Livre, Membre, Emprunt, StatutEmprunt
from utils.database import db_manager
from datetime import datetime, timedelta

livres_bp = Blueprint('livres', __name__)

@livres_bp.route('/livres')
def liste_livres():
    session = db_manager.get_session()
    livres = session.query(Livre).all()
    return render_template('livres.html', livres=livres)

@livres_bp.route('/livre/<int:livre_id>')
def livre_details(livre_id):
    session = db_manager.get_session()
    livre = session.query(Livre).get(livre_id)
    membres_actifs = session.query(Membre).all()
    return render_template('livre_details.html', livre=livre, membres_actifs=membres_actifs)

@livres_bp.route('/ajouter_livre', methods=['POST'])
def ajouter_livre():
    session = db_manager.get_session()
    livre = Livre(
        titre=request.form['titre'],
        auteur=request.form['auteur'],
        isbn=request.form['isbn']
    )
    session.add(livre)
    session.commit()
    return redirect(url_for('livres.liste_livres'))

@livres_bp.route('/emprunter_livre/<int:livre_id>', methods=['POST'])
def emprunter_livre(livre_id):
    session = db_manager.get_session()
    membre_id = request.form.get('membre_id')

    livre = session.query(Livre).get(livre_id)
    if not livre or not livre.disponible:
        return jsonify({'success': False, 'message': 'Livre non disponible'})

    # Création de l'emprunt
    emprunt = Emprunt(
        livre_id=livre_id,
        membre_id=membre_id,
        date_retour_prevue=datetime.now() + timedelta(days=14),
        statut=StatutEmprunt.EN_COURS
    )
    livre.disponible = False

    session.add(emprunt)
    session.commit()

    return redirect(url_for('livres.livre_details', livre_id=livre_id))
