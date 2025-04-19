import os
from dotenv import load_dotenv

load_dotenv()  # Load from .env


class Config:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Config, cls).__new__(cls)
            cls._instance.load_config()
        return cls._instance

    def load_config(self):
        self.DATABASE_URL = os.getenv(
            "DATABASE_URL",
            "postgresql://postgres:1234@localhost:5432/opentable",
        )
        self.SECRET_KEY = os.getenv("SECRET_KEY", "fallback-secret-key")
        self.ALGORITHM = os.getenv("ALGORITHM", "HS256")
        self.ACCESS_TOKEN_EXPIRE_MINUTES = int(
            os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60)
        )


config = Config()
