from models import Base
from utils.database import db_manager
from models import Livre, Membre

def init_database():
    # Création des tables
    db_manager.init_db()
    
    # Création d'un jeu de données initial
    session = db_manager.get_session()
    
    # Ajout de quelques livres
    livres = [
        Livre(titre="1984", auteur="George Orwell", isbn="9780451524935"),
        Livre(titre="Le Petit Prince", auteur="Antoine de Saint-Exupéry", isbn="9782070612758"),
    ]
    session.add_all(livres)
    
    # Ajout de quelques membres
    membres = [
        Membre(nom="Dupont", prenom="Jean", email="jean.dupont@email.com"),
        Membre(nom="Martin", prenom="Marie", email="marie.martin@email.com"),
    ]
    session.add_all(membres)
    
    session.commit()

if __name__ == "__main__":
    init_database() 