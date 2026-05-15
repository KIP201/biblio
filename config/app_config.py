import os
from datetime import timedelta

class DatabaseConfig:
    def __init__(self):
        self.type = 'sqlite'
        self.name = 'bibliotheque.db'
        self.url = f'sqlite:///{self.name}'

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-key-123'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///bibliotheque.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    DEBUG = False
    BACKUP_DIR = 'backups'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max-size

    # Configuration de la session
    PERMANENT_SESSION_LIFETIME = timedelta(days=1)
    SESSION_TYPE = 'filesystem'
    SESSION_FILE_DIR = 'flask_session'

    def __init__(self):
        self.database = DatabaseConfig()
        self.debug = self.DEBUG
