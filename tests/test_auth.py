import unittest
from unittest.mock import patch
from main import create_app
from models import User, UserRole
from utils.database import db_manager
from werkzeug.security import generate_password_hash
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
            password=generate_password_hash('test_password'),
            role=UserRole.ADMIN
        )
        session.add(user)
        session.commit()
    
    def test_login_success(self):
        response = self.client.post('/login', data={
            'username': 'test_user',
            'password': 'test_password'
        }, follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Login successful', response.data)
    
    def test_login_failure(self):
        response = self.client.post('/login', data={
            'username': 'test_user',
            'password': 'wrong_password'
        }, follow_redirects=True)
        self.assertIn(b'Invalid credentials', response.data)
    
    def test_logout(self):
        # Login first
        self.client.post('/login', data={
            'username': 'test_user',
            'password': 'test_password'
        })
        
        # Then logout
        response = self.client.get('/logout', follow_redirects=True)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Logged out successfully', response.data)
    
    def test_protected_route(self):
        # Test sans authentification
        response = self.client.get('/admin', follow_redirects=True)
        self.assertIn(b'Please log in', response.data)
        
        # Test avec authentification
        self.client.post('/login', data={
            'username': 'test_user',
            'password': 'test_password'
        })
        response = self.client.get('/admin')
        self.assertEqual(response.status_code, 200)
    
    def test_role_required(self):
        # Test avec un rôle insuffisant
        with patch('models.user.UserRole') as mock_role:
            mock_role.ADMIN = 'ADMIN'
            mock_role.USER = 'USER'
            
            user = User(username='basic_user', password='pass', role='USER')
            session = db_manager.get_session()
            session.add(user)
            session.commit()
            
            self.client.post('/login', data={
                'username': 'basic_user',
                'password': 'pass'
            })
            
            response = self.client.get('/admin')
            self.assertEqual(response.status_code, 403)
    
    def test_session_timeout(self):
        with patch('datetime.datetime') as mock_datetime:
            # Simuler une session expirée
            mock_datetime.now.return_value = datetime(2024, 1, 1, 12, 0)
            self.client.post('/login', data={
                'username': 'test_user',
                'password': 'test_password'
            })
            
            # Avancer le temps
            mock_datetime.now.return_value = datetime(2024, 1, 2, 12, 0)
            response = self.client.get('/admin', follow_redirects=True)
            self.assertIn(b'Session expired', response.data)
    
    def tearDown(self):
        session = db_manager.get_session()
        session.query(User).delete()
        session.commit()
        self.app_context.pop() 