import unittest
from main import create_app
from models import Livre, Membre
from utils.database import db_manager

class TestSearch(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        session = db_manager.get_session()
        
        # Ajout de plusieurs livres pour les tests de recherche
        livres = [
            Livre(titre="Python Programming", auteur="John Doe", isbn="1111111111111"),
            Livre(titre="Flask Web Dev", auteur="Jane Smith", isbn="2222222222222"),
            Livre(titre="Database Design", auteur="John Doe", isbn="3333333333333")
        ]
        session.add_all(livres)
        session.commit()
    
    def test_search_by_title(self):
        response = self.client.get('/livres?search=Python')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Python Programming', response.data)
        self.assertNotIn(b'Flask Web Dev', response.data)
    
    def test_search_by_author(self):
        response = self.client.get('/livres?search=John+Doe')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Python Programming', response.data)
        self.assertIn(b'Database Design', response.data)
    
    def test_search_no_results(self):
        response = self.client.get('/livres?search=NonExistent')
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'No results found', response.data)
    
    def tearDown(self):
        session = db_manager.get_session()
        session.query(Livre).delete()
        session.commit()
        self.app_context.pop() 