from .database import DatabaseManager


class DatabaseStorage:
    def __init__(self):
        self.db = DatabaseManager()
