from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import os

load_dotenv()


class AppSettings(BaseSettings):
    app_name: str = os.getenv('APP_NAME')
    secret: str = os.getenv("SECRET")


class DBSettings(BaseSettings):
    db_port: str = os.getenv('DB_PORT')
    db_user: str = os.getenv("PG_USER")
    db_pass: str = os.getenv("PG_PASSWORD")
    db_host: str = os.getenv("PG_HOST")
    db_name: str = os.getenv("PG_DB")
    sqlalchemy_url: str = os.getenv("SQLALCHEMY_URL")


settings = AppSettings()
db_settings = DBSettings()