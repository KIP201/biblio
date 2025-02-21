from datetime import datetime
from utils.logger import logger

class NotificationManager:
    def __init__(self):
        self.notifications = []
    
    def envoyer_notification_retard(self, emprunt):
        message = f"Le livre '{emprunt.livre.titre}' emprunté par {emprunt.membre.prenom} {emprunt.membre.nom} est en retard"
        logger.warning(message)
        self.notifications.append({
            'type': 'retard',
            'message': message,
            'date': datetime.now(),
            'lu': False
        })
    
    def envoyer_notification_amende(self, amende):
        message = f"Une amende de {amende.montant}€ a été créée pour {amende.emprunt.membre.prenom} {amende.emprunt.membre.nom}"
        logger.info(message)
        self.notifications.append({
            'type': 'amende',
            'message': message,
            'date': datetime.now(),
            'lu': False
        })

notification_manager = NotificationManager() 