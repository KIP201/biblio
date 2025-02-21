import os
import shutil
from datetime import datetime
from utils.logger import logger

class BackupManager:
    def __init__(self, backup_dir="backups"):
        self.backup_dir = backup_dir
        if not os.path.exists(backup_dir):
            os.makedirs(backup_dir)
    
    def create_backup(self, db_file):
        try:
            # Création du nom du fichier de backup avec timestamp
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_name = f"backup_{timestamp}.db"
            backup_path = os.path.join(self.backup_dir, backup_name)
            
            # Copie du fichier de base de données
            shutil.copy2(db_file, backup_path)
            
            # Nettoyage des vieux backups (garde les 5 plus récents)
            self._cleanup_old_backups()
            
            logger.info(f"Backup créé avec succès: {backup_name}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de la création du backup: {str(e)}")
            return False
    
    def _cleanup_old_backups(self, keep_count=5):
        try:
            # Liste tous les fichiers de backup
            backups = sorted([
                f for f in os.listdir(self.backup_dir)
                if f.startswith("backup_") and f.endswith(".db")
            ])
            
            # Supprime les plus vieux si nécessaire
            while len(backups) > keep_count:
                oldest = backups.pop(0)
                os.remove(os.path.join(self.backup_dir, oldest))
                logger.info(f"Ancien backup supprimé: {oldest}")
                
        except Exception as e:
            logger.error(f"Erreur lors du nettoyage des backups: {str(e)}")

backup_manager = BackupManager() 