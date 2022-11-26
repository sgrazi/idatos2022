from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

POSTGRES_URL = "postgresql://admin:admin@localhost:5432/idatos2022" #"postgresql://postgres:master@localhost:5432/idatos2022"


class SingletonDatabase:
    __instance = None

    @staticmethod
    def get_instance():
        """Static access method."""
        if SingletonDatabase.__instance == None:
            SingletonDatabase()
        return SingletonDatabase.__instance

    def __init__(self):
        """Virtually private constructor."""
        if SingletonDatabase.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            ### para testear activar echo=True
            # self.engine = create_engine(POSTGRES_URL, echo=True)
            self.engine = create_engine(POSTGRES_URL)
            self.Base = declarative_base(self.engine)
            Session = sessionmaker(bind=self.engine)
            self.session = Session()
            SingletonDatabase.__instance = self
