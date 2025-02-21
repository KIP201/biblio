import unittest
from main import create_app
from models import Livre, Membre, Emprunt
from utils.database import db_manager
from datetime import datetime, timedelta

class TestLivres(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Création des données de test
        session = db_manager.get_session()
        
        # Ajout d'un livre
        self.livre = Livre(
            titre="Test Livre",
            auteur="Test Auteur",
            isbn="1234567890123"
        )
        session.add(self.livre)
        
        # Ajout d'un membre
        self.membre = Membre(
            nom="Test",
            prenom="User",
            email="test@test.com"
        )
        session.add(self.membre)
        
        session.commit()
    
    def test_liste_livres(self):
        response = self.client.get('/livres')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Livre', response.data)
    
    def test_details_livre(self):
        response = self.client.get(f'/livre/{self.livre.id}')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Test Auteur', response.data)
    
    def test_emprunt_livre(self):
        response = self.client.post(f'/emprunter_livre/{self.livre.id}', data={
            'membre_id': self.membre.id
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        # Vérification que le livre n'est plus disponible
        session = db_manager.get_session()
        livre = session.query(Livre).get(self.livre.id)
        self.assertFalse(livre.disponible)
    
    def tearDown(self):
        session = db_manager.get_session()
        session.query(Emprunt).delete()
        session.query(Livre).delete()
        session.query(Membre).delete()
        session.commit()
        self.app_context.pop() 