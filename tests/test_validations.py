import unittest
from main import create_app
from models import Livre, Membre, Emprunt
from utils.database import db_manager
from datetime import datetime

class TestValidations(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def test_isbn_validation(self):
        response = self.client.post('/ajouter_livre', data={
            'titre': 'Test Livre',
            'auteur': 'Test Auteur',
            'isbn': '123'  # ISBN invalide
        }, follow_redirects=True)
        self.assertIn(b'Invalid ISBN', response.data)
    
    def test_email_validation(self):
        response = self.client.post('/ajouter_membre', data={
            'nom': 'Test',
            'prenom': 'User',
            'email': 'invalid-email'  # Email invalide
        }, follow_redirects=True)
        self.assertIn(b'Invalid email', response.data)
    
    def test_duplicate_isbn(self):
        session = db_manager.get_session()
        livre = Livre(titre="Test", auteur="Test", isbn="1234567890123")
        session.add(livre)
        session.commit()
        
        response = self.client.post('/ajouter_livre', data={
            'titre': 'Autre Livre',
            'auteur': 'Autre Auteur',
            'isbn': '1234567890123'  # ISBN déjà utilisé
        }, follow_redirects=True)
        self.assertIn(b'ISBN already exists', response.data)
    
    def tearDown(self):
        session = db_manager.get_session()
        session.query(Livre).delete()
        session.commit()
        self.app_context.pop() 