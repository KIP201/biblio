from flask import Blueprint, render_template, redirect, url_for, request
from models import Amende, StatutAmende, ModePaiement
from utils.database import db_manager
from datetime import datetime

amendes_bp = Blueprint('amendes', __name__)

@amendes_bp.route('/amendes')
def liste_amendes():
    session = db_manager.get_session()
    amendes = session.query(Amende).order_by(Amende.date_creation.desc()).all()
    return render_template('amendes.html', amendes=amendes)

@amendes_bp.route('/amende/<int:amende_id>/payer', methods=['POST'])
def payer_amende(amende_id):
    session = db_manager.get_session()
    amende = session.query(Amende).get(amende_id)
    
    if amende and amende.statut == StatutAmende.EN_ATTENTE:
        amende.statut = StatutAmende.PAYEE
        amende.date_paiement = datetime.now()
        amende.mode_paiement = ModePaiement[request.form['mode_paiement']]
        session.commit()
    
    return redirect(url_for('amendes.liste_amendes')) 