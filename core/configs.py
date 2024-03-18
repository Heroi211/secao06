from typing import List, Annotated, TypeVar
from sqlalchemy.ext.declarative import declarative_base
from pydantic.v1 import BaseSettings
import os 
from pydantic import Field

class Settings(BaseSettings):
    API_V3_VERSION : str = '/api/v3'
    DB_URL = "postgresql+asyncpg://hero:280387@localhost:5432/API"
    DBBaseModel = declarative_base()
    
    JWT_SECRET:str = os.getenv('SECRET')
    """
        import secrets
        token : str = secrets.token_urlsafe(32)
    """
    
    ALGORITH: str='HS256'
    ACCESS_TOKEN_EXPIRE_MINUTES: int = (60*24*7) #10080
    
    class Config:
        case_sensitive = True
        
settings: Settings = Settings()
