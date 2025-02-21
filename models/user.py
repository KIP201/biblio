from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
import enum
from models import Base

class UserRole(enum.Enum):
    ADMIN = "ADMIN"
    BIBLIOTHECAIRE = "BIBLIOTHECAIRE"
    MEMBRE = "MEMBRE"

class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(256))
    role = Column(Enum(UserRole), default=UserRole.MEMBRE)
    active = Column(Boolean, default=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password) 