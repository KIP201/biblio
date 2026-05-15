from flask import Blueprint, render_template, redirect, url_for, request, flash, session as flask_session
from models.user import User
from utils.database import db_manager
from utils.logger import logger

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        db_session = db_manager.get_session()
        user = db_session.query(User).filter_by(username=username).first()

        if user and user.check_password(password):
            flask_session['user_id'] = user.id
            flask_session['user_roles'] = [user.role.value]
            flash('Connexion réussie!', 'success')
            return redirect(url_for('main.home'))

        flash('Identifiants invalides.', 'error')

    return render_template('auth/login.html')

@auth_bp.route('/logout')
def logout():
    flask_session.clear()
    flash('Vous avez été déconnecté.', 'info')
    return redirect(url_for('main.home'))
