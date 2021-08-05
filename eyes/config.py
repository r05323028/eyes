'''Eyes config
'''
from pydantic import BaseSettings, Field


class DatabaseConfig(BaseSettings):
    '''Database config

    Attributes:
        host (str): database host
        port (int): database port
        username (str): database username
        password (str): database password
        database (str): database name
    '''
    host: str
    port: int = Field(3306)
    username: str
    password: str
    database: str = Field('eyes')

    class Config:
        env_prefix = 'MYSQL_'


class CeleryConfig(BaseSettings):
    '''Celery config

    Attributes:
        broker_url (str): celery broker url
        result_backend (str): celery result backend
    '''
    broker_url: str
    result_backend: str

    class Config:
        env_prefix = 'CELERY_'
