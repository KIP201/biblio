import unittest
import time
from main import create_app
from models import Livre
from utils.database import db_manager

class TestPerformance(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def test_search_performance(self):
        session = db_manager.get_session()
        
        # Ajout de 100 livres
        for i in range(100):
            livre = Livre(
                titre=f"Book {i}",
                auteur=f"Author {i}",
                isbn=f"{i:013d}"
            )
            session.add(livre)
        session.commit()
        
        # Test de performance de la recherche
        start_time = time.time()
        response = self.client.get('/livres?search=Book')
        end_time = time.time()
        
        # La recherche devrait prendre moins de 0.5 secondes
        self.assertLess(end_time - start_time, 0.5)
        self.assertEqual(response.status_code, 200)
    
    def tearDown(self):
        session = db_manager.get_session()
        session.query(Livre).delete()
        session.commit()
        self.app_context.pop() 