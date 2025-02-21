import csv
import json
from datetime import datetime
from models import Livre, Membre, Emprunt
from utils.database import db_manager
from utils.logger import logger

class DataManager:
    def export_to_csv(self, model_class, filename):
        """Exporte les données d'un modèle vers un fichier CSV"""
        try:
            session = db_manager.get_session()
            items = session.query(model_class).all()
            
            if not items:
                logger.warning(f"Aucune donnée à exporter pour {model_class.__name__}")
                return False
            
            # Obtenir les noms des colonnes
            columns = [column.name for column in model_class.__table__.columns]
            
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=columns)
                writer.writeheader()
                
                for item in items:
                    row = {column: getattr(item, column) for column in columns}
                    writer.writerow(row)
                    
            logger.info(f"Export CSV réussi: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors de l'export CSV: {str(e)}")
            return False

    def import_from_csv(self, model_class, filename):
        """Importe les données d'un fichier CSV vers un modèle"""
        try:
            session = db_manager.get_session()
            
            with open(filename, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    # Convertir les types de données si nécessaire
                    for key, value in row.items():
                        if 'date' in key.lower() and value:
                            row[key] = datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
                        elif value == 'None':
                            row[key] = None
                    
                    item = model_class(**row)
                    session.add(item)
                    
            session.commit()
            logger.info(f"Import CSV réussi: {filename}")
            return True
            
        except Exception as e:
            session.rollback()
            logger.error(f"Erreur lors de l'import CSV: {str(e)}")
            return False

    def export_full_backup(self, filename):
        """Exporte toutes les données de la base dans un fichier JSON"""
        try:
            data = {
                'livres': self.export_to_dict(Livre),
                'membres': self.export_to_dict(Membre),
                'emprunts': self.export_to_dict(Emprunt)
            }
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2, default=str)
                
            logger.info(f"Backup complet exporté: {filename}")
            return True
            
        except Exception as e:
            logger.error(f"Erreur lors du backup complet: {str(e)}")
            return False

    def export_to_dict(self, model_class):
        """Convertit les données d'un modèle en dictionnaire"""
        session = db_manager.get_session()
        items = session.query(model_class).all()
        return [item.to_dict() for item in items]

data_manager = DataManager() 