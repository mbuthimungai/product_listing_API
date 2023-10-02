# import packages
from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv
import secrets

load_dotenv()
class Settings(BaseSettings):
    """
    Application settings and configurations parameters
    
    This class defines app settings using pydantic a data validation library
    """
    PROJECT_NAME: str = os.getenv("PROJECT_NAME")
    API_V1_STR: str = "/api/v1"
    ASYNC_DATABASE_URI: str = os.getenv("ASYNC_DATABASE_URI")
    SECRET_KEY: str = secrets.token_urlsafe(32)
    
    
settings = Settings()