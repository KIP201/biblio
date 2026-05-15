from sqlalchemy import Column, Integer, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from models import Base

class StatutEmprunt(enum.Enum):
    EN_COURS = "EN_COURS"
    RENDU = "RENDU"
    EN_RETARD = "EN_RETARD"

class Emprunt(Base):
    __tablename__ = 'emprunts'

    id = Column(Integer, primary_key=True)
    livre_id = Column(Integer, ForeignKey('livres.id'), nullable=False)
    membre_id = Column(Integer, ForeignKey('membres.id'), nullable=False)
    date_emprunt = Column(DateTime, default=datetime.now)
    date_retour_prevue = Column(DateTime, nullable=False)
    date_retour_effective = Column(DateTime)
    statut = Column(Enum(StatutEmprunt), default=StatutEmprunt.EN_COURS)

    livre = relationship("Livre")
    membre = relationship("Membre", back_populates="emprunts")

    def __init__(self, **kwargs):
        super(Emprunt, self).__init__(**kwargs)
        if self.statut is None:
            self.statut = StatutEmprunt.EN_COURS
        if self.date_emprunt is None:
            self.date_emprunt = datetime.now()

    def __repr__(self):
        return f"<Emprunt livre_id={self.livre_id} membre_id={self.membre_id}>"
