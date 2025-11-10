from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

from data.models import *



class DatabaseManager:
    def __init__(self, connection_string='sqlite:///ANSDatabase.db'):
        self.engine = create_engine(connection_string)
        self.session = sessionmaker(autocommit=False,
                                          autoflush=False,
                                          bind=self.engine,
                                          expire_on_commit=False
                                          )
        Base.metadata.create_all(self.engine)

    @contextmanager
    def get_session(self):
        session = self.session()
        try:
            yield session
            session.commit()
        except:
            session.rollback()
            raise
        finally:
            session.close()

db = DatabaseManager()
