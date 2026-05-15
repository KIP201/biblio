import unittest
from unittest.mock import patch
from main import create_app
from models import User, UserRole
from utils.database import db_manager
from datetime import datetime

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Création d'un utilisateur de test
        session = db_manager.get_session()
        user = User(
            username='test_user',
            email='test@example.com',
            role=UserRole.ADMIN
        )
        user.set_password('test_password')
        session.add(user)
        session.commit()

    def test_login_success(self):
        response = self.client.post('/login', data={
            'username': 'test_user',
            'password': 'test_password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Connexion r\xc3\xa9ussie!', response.data)

    def test_login_failure(self):
        response = self.client.post('/login', data={
            'username': 'test_user',
            'password': 'wrong_password'
        }, follow_redirects=True)
        self.assertIn(b'Identifiants invalides.', response.data)

    def test_logout(self):
        # Login first
        self.client.post('/login', data={
            'username': 'test_user',
            'password': 'test_password'
        })

        # Then logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Vous avez \xc3\xa9t\xc3\xa9 d\xc3\xa9connect\xc3\xa9.', response.data)

    def tearDown(self):
        session = db_manager.get_session()
        session.query(User).delete()
        session.commit()
        self.app_context.pop()
