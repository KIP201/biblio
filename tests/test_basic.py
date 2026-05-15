import unittest
from main import create_app
from utils.database import db_manager

class TestBasicFunctionality(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app.testing = True

    def test_home_page(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_livres_page(self):
        response = self.client.get('/livres')
        self.assertEqual(response.status_code, 200)

if __name__ == '__main__':
    unittest.main()
