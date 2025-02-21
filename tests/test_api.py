import unittest
import json
from main import create_app
from models import Livre
from utils.database import db_manager

class TestAPI(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Ajout de données de test
        session = db_manager.get_session()
        livre = Livre(
            titre="API Test Book",
            auteur="API Author",
            isbn="9999999999999"
        )
        session.add(livre)
        session.commit()
        self.livre_id = livre.id
    
    def test_get_livre_api(self):
        response = self.client.get(f'/api/livre/{self.livre_id}')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['titre'], "API Test Book")
    
    def test_create_livre_api(self):
        livre_data = {
            'titre': 'New Book',
            'auteur': 'New Author',
            'isbn': '8888888888888'
        }
        response = self.client.post('/api/livre',
                                  data=json.dumps(livre_data),
                                  content_type='application/json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.data)
        self.assertEqual(data['titre'], "New Book")
    
    def tearDown(self):
        session = db_manager.get_session()
        session.query(Livre).delete()
        session.commit()
        self.app_context.pop() 