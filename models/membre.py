from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from models import Base

class Membre(Base):
    __tablename__ = 'membres'

    id = Column(Integer, primary_key=True)
    nom = Column(String(50), nullable=False)
    prenom = Column(String(50), nullable=False)
    email = Column(String(120), unique=True, nullable=False)

    emprunts = relationship("Emprunt", back_populates="membre")

    def __repr__(self):
        return f"<Membre {self.prenom} {self.nom}>"
