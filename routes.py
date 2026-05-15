from flask import render_template, redirect, url_for, request, jsonify
from models import Livre, Membre, Emprunt, StatutEmprunt
from utils.database import db_manager
from datetime import datetime, timedelta

def init_routes(app):
    # Les routes ont été déplacées dans routes/main.py, routes/livres.py, etc.
    pass
