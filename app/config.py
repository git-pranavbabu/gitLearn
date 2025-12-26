from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os
load_dotenv()

class Settings(BaseSettings):
    DATABASE_HOST: str = os.getenv("DATABASE_HOST")
    DATABASE_PORT: int = os.getenv("DATABASE_PORT")
    DATABASE_NAME: str = os.getenv("DATABASE_NAME")
    DATABASE_USER: str = os.getenv("DATABASE_USER")
    DATABASE_PASSWORD: str = os.getenv("DATABASE_PASSWORD")
    SECRET_KEY: str = os.getenv("SECRET_KEY")
    ALGORITHM: str = os.getenv("ALGORITHM")
    EXPIRE_IN: int = os.getenv("EXPIRE_IN")

settings = Settings()