import unittest
from models import Livre, Membre, Emprunt, Amende
from datetime import datetime, timedelta

class TestModels(unittest.TestCase):
    def setUp(self):
        self.livre = Livre(
            titre="Test Livre",
            auteur="Test Auteur",
            isbn="1234567890123"
        )
        
        self.membre = Membre(
            nom="Test",
            prenom="User",
            email="test@test.com"
        )
        
        self.emprunt = Emprunt(
            livre_id=1,
            membre_id=1,
            date_retour_prevue=datetime.now() + timedelta(days=14)
        )

    def test_livre_creation(self):
        self.assertEqual(self.livre.titre, "Test Livre")
        self.assertTrue(self.livre.disponible)

    def test_membre_creation(self):
        self.assertEqual(self.membre.email, "test@test.com")

    def test_emprunt_creation(self):
        self.assertEqual(self.emprunt.statut.value, "EN_COURS") 