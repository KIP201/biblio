import unittest
from main import app
from utils.database import db_manager

class TestBasicFunctionality(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        db_manager.init_db()

    def test_home_page(self):
        response = self.app.get('/')
        self.assertEqual(response.status_code, 200)

    def test_livres_page(self):
        response = self.app.get('/livres')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main() 