from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dependencies.config import Config

Base = declarative_base()


class Database:
    _instance = None

    def __init__(self):
        if Database._instance is None:
            config = Config()
            engine = create_engine(config.DATABASE_URL)
            self.SessionLocal = sessionmaker(
                autocommit=False, autoflush=False, bind=engine
            )  # Use SessionLocal here
            self.engine = engine  # Keep engine for reference if needed
            Database._instance = self
        else:
            raise Exception("Singleton violation")

    @staticmethod
    def get_instance():
        if Database._instance is None:
            Database()
        return Database._instance


# ✅ Updated function to use SessionLocal
def get_db():
    db = Database.get_instance().SessionLocal()  # Get session from singleton
    try:
        yield db
    finally:
        db.close()
