import os
from dotenv import load_dotenv
from pathlib import Path

env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

class Settings:
    PROJECT_NAME:str = 'TPMELI'
    PROJECT_VERSION:str = '1.0'
    MONGO_DB:str = os.getenv('MONGO_DB')

settings = Settings()