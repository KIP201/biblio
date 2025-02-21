from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from models import Base
from config import config
from utils.logger import logger
from utils.backup import backup_manager
import os

class DatabaseManager:
    def __init__(self):
        self.engine = None
        self.Session = None
        self._current_session = None
    
    def init_db(self):
        try:
            # Création du dossier de la base de données si nécessaire
            db_dir = os.path.dirname(config.database.name)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)
            
            # Initialisation du moteur SQLAlchemy
            self.engine = create_engine(
                config.database.url,
                echo=config.debug,
                pool_pre_ping=True
            )
            
            # Création des tables
            Base.metadata.create_all(self.engine)
            
            # Configuration de la session
            self.Session = sessionmaker(bind=self.engine)
            
            logger.info("Base de données initialisée avec succès")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'initialisation de la base de données: {str(e)}")
            return False
    
    def get_session(self):
        if not self._current_session:
            self._current_session = self.Session()
        return self._current_session
    
    def close_session(self):
        if self._current_session:
            self._current_session.close()
            self._current_session = None
    
    def backup_db(self, backup_dir=None):
        try:
            if not backup_dir:
                backup_dir = config.BACKUP_DIR
            return backup_manager.create_backup(config.database.name)
        except Exception as e:
            logger.error(f"Erreur lors de la sauvegarde: {str(e)}")
            return False

db_manager = DatabaseManager() 