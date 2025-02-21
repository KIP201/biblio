import unittest
from main import create_app
from models import Livre
from utils.database import db_manager

class TestErrorHandlers(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
    
    def test_404_error(self):
        response = self.client.get('/page_inexistante')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Page not found', response.data)
    
    def test_500_error(self):
        # Simulation d'une erreur interne
        @self.app.route('/force_error')
        def force_error():
            raise Exception("Test error")
        
        response = self.client.get('/force_error')
        self.assertEqual(response.status_code, 500)
        self.assertIn(b'Internal server error', response.data)
    
    def test_invalid_id(self):
        response = self.client.get('/livre/999999')
        self.assertEqual(response.status_code, 404)
        self.assertIn(b'Book not found', response.data)
    
    def tearDown(self):
        self.app_context.pop() 