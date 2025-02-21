from sqlalchemy import Column, Integer, Float, DateTime, ForeignKey, Enum, String
from sqlalchemy.orm import relationship
import enum
from datetime import datetime
from models import Base

class StatutAmende(enum.Enum):
    EN_ATTENTE = "EN_ATTENTE"
    PAYEE = "PAYEE"
    ANNULEE = "ANNULEE"

class ModePaiement(enum.Enum):
    ESPECES = "ESPECES"
    CHEQUE = "CHEQUE"

class Amende(Base):
    __tablename__ = 'amendes'
    
    id = Column(Integer, primary_key=True)
    emprunt_id = Column(Integer, ForeignKey('emprunts.id'), nullable=False)
    montant = Column(Float, nullable=False)
    date_creation = Column(DateTime, default=datetime.now, nullable=False)
    date_paiement = Column(DateTime)
    statut = Column(Enum(StatutAmende), default=StatutAmende.EN_ATTENTE)
    mode_paiement = Column(Enum(ModePaiement))
    commentaire = Column(String(200))
    
    emprunt = relationship("Emprunt", backref="amendes") 