from datetime import timedelta

# Configuration des emprunts
DUREE_EMPRUNT = timedelta(days=14)
MONTANT_AMENDE_PAR_JOUR = 0.50
MAX_EMPRUNTS_PAR_MEMBRE = 5
DUREE_MAX_PROLONGATION = timedelta(days=7)

# Configuration des sauvegardes
BACKUP_RETENTION_DAYS = 30
MAX_BACKUP_SIZE = 100 * 1024 * 1024  # 100MB

# Configuration de l'interface
ITEMS_PER_PAGE = 20
MAX_SEARCH_RESULTS = 100
SESSION_DURATION = timedelta(hours=8)

# Messages d'erreur
MESSAGES = {
    'LIVRE_NON_DISPONIBLE': "Ce livre n'est pas disponible actuellement.",
    'LIMITE_EMPRUNTS': "Vous avez atteint la limite d'emprunts autorisée.",
    'RETARD_EXISTANT': "Vous avez des emprunts en retard. Veuillez les régulariser.",
    'AMENDE_IMPAYEE': "Vous avez des amendes impayées. Veuillez les régler.",
}

# Statuts
STATUTS_EMPRUNT = ['EN_COURS', 'RETOURNE', 'EN_RETARD']
STATUTS_AMENDE = ['EN_ATTENTE', 'PAYEE', 'ANNULEE']
MODES_PAIEMENT = ['ESPECES', 'CHEQUE'] 