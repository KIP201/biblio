from flask import Blueprint, render_template, redirect, url_for, request, flash
from models import Membre
from utils.database import db_manager

membres_bp = Blueprint('membres', __name__)

@membres_bp.route('/membres')
def liste_membres():
    session = db_manager.get_session()
    membres = session.query(Membre).all()
    return render_template('membres.html', membres=membres)

@membres_bp.route('/ajouter_membre', methods=['POST'])
def ajouter_membre():
    session = db_manager.get_session()

    nom = request.form.get('nom')
    prenom = request.form.get('prenom')
    email = request.form.get('email')

    # Vérifier si l'email existe déjà
    existant = session.query(Membre).filter_by(email=email).first()
    if existant:
        flash('Cet email est déjà utilisé.', 'error')
        return redirect(url_for('membres.liste_membres'))

    nouveau_membre = Membre(
        nom=nom,
        prenom=prenom,
        email=email
    )

    session.add(nouveau_membre)
    session.commit()

    flash(f'Membre {prenom} {nom} ajouté avec succès.', 'success')
    return redirect(url_for('membres.liste_membres'))
