import os

class Config:
    def __init__(self):
        self.debug = False
        self.database = DatabaseConfig()

class DatabaseConfig:
    def __init__(self):
        self.type = 'sqlite'
        self.name = 'bibliotheque.db'
        self.url = f'sqlite:///{self.name}'

config = Config() 