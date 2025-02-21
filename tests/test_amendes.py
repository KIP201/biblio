import unittest
from main import create_app
from models import Livre, Membre, Emprunt, Amende, StatutEmprunt, StatutAmende
from utils.database import db_manager
from datetime import datetime, timedelta

class TestAmendes(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        session = db_manager.get_session()
        
        # Création d'un emprunt en retard
        self.livre = Livre(titre="Test Livre", auteur="Test Auteur", isbn="1234567890123")
        self.membre = Membre(nom="Test", prenom="User", email="test@test.com")
        session.add_all([self.livre, self.membre])
        session.commit()
        
        self.emprunt = Emprunt(
            livre_id=self.livre.id,
            membre_id=self.membre.id,
            date_emprunt=datetime.now() - timedelta(days=30),
            date_retour_prevue=datetime.now() - timedelta(days=15),
            statut=StatutEmprunt.EN_RETARD
        )
        session.add(self.emprunt)
        
        self.amende = Amende(
            emprunt_id=self.emprunt.id,
            montant=7.50,
            date_creation=datetime.now()
        )
        session.add(self.amende)
        session.commit()
    
    def test_liste_amendes(self):
        response = self.client.get('/amendes')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'7.50', response.data)
    
    def test_payer_amende(self):
        response = self.client.post(f'/amende/{self.amende.id}/payer', data={
            'mode_paiement': 'ESPECES'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        
        session = db_manager.get_session()
        amende = session.query(Amende).get(self.amende.id)
        self.assertEqual(amende.statut, StatutAmende.PAYEE)
    
    def tearDown(self):
        session = db_manager.get_session()
        session.query(Amende).delete()
        session.query(Emprunt).delete()
        session.query(Livre).delete()
        session.query(Membre).delete()
        session.commit()
        self.app_context.pop() 