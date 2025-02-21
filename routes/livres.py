from flask import Blueprint, render_template, redirect, url_for, request, jsonify
from models import Livre, Membre, Emprunt
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