from sqlalchemy import Column, Integer, String, Boolean
from models import Base

class Livre(Base):
    __tablename__ = 'livres'

    id = Column(Integer, primary_key=True)
    titre = Column(String(200), nullable=False)
    auteur = Column(String(100), nullable=False)
    isbn = Column(String(13), unique=True, nullable=False)
    disponible = Column(Boolean, default=True)

    def __init__(self, **kwargs):
        super(Livre, self).__init__(**kwargs)
        if self.disponible is None:
            self.disponible = True

    def __repr__(self):
        return f"<Livre {self.titre}>"
