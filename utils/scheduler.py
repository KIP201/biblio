import schedule
import time
import threading
from datetime import datetime, timedelta
from utils.database import db_manager
from utils.notifications import notification_manager
from utils.backup import backup_manager
from models import Emprunt, StatutEmprunt, Amende
from utils.logger import logger

class TaskScheduler:
    def __init__(self):
        self.running = False
        self.thread = None
        self.tasks = []
    
    def add_task(self, task, schedule_time):
        """Ajoute une tâche planifiée"""
        self.tasks.append((task, schedule_time))
        if isinstance(schedule_time, str):
            schedule.every().day.at(schedule_time).do(task)
        elif isinstance(schedule_time, int):
            schedule.every(schedule_time).minutes.do(task)
    
    def start(self):
        """Démarre le planificateur"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._run, daemon=True)
            self.thread.start()
            logger.info("Planificateur démarré")
    
    def stop(self):
        """Arrête le planificateur"""
        self.running = False
        if self.thread:
            self.thread.join()
            logger.info("Planificateur arrêté")
    
    def _run(self):
        """Boucle principale du planificateur"""
        while self.running:
            try:
                schedule.run_pending()
                time.sleep(60)
            except Exception as e:
                logger.error(f"Erreur dans le planificateur: {str(e)}")
                time.sleep(300)  # Attendre 5 minutes en cas d'erreur
    
    def check_overdue(self):
        """Vérifie les emprunts en retard"""
        session = db_manager.get_session()
        try:
            overdue = session.query(Emprunt)\
                .filter(Emprunt.statut == StatutEmprunt.EN_COURS)\
                .filter(Emprunt.date_retour_prevue < datetime.now())\
                .all()
            
            for emprunt in overdue:
                self._handle_overdue_loan(emprunt, session)
                
            session.commit()
            logger.info(f"{len(overdue)} emprunts en retard traités")
            
        except Exception as e:
            logger.error(f"Erreur lors de la vérification des retards: {str(e)}")
            session.rollback()
        finally:
            session.close()
    
    def _handle_overdue_loan(self, emprunt, session):
        """Gère un emprunt en retard"""
        try:
            # Calcul des jours de retard
            days_overdue = (datetime.now() - emprunt.date_retour_prevue).days
            fine_amount = days_overdue * 0.50  # 50 centimes par jour
            
            # Création de l'amende si pas déjà existante
            if not session.query(Amende).filter_by(emprunt_id=emprunt.id).first():
                amende = Amende(
                    emprunt_id=emprunt.id,
                    montant=fine_amount,
                    commentaire=f"Retard de {days_overdue} jours"
                )
                session.add(amende)
                notification_manager.envoyer_notification_amende(amende)
            
            emprunt.statut = StatutEmprunt.EN_RETARD
            notification_manager.envoyer_notification_retard(emprunt)
            
        except Exception as e:
            logger.error(f"Erreur lors du traitement de l'emprunt {emprunt.id}: {str(e)}")
            raise

scheduler = TaskScheduler() 