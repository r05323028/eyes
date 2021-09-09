'''Eyes config
'''
import typing

from pydantic import BaseSettings, Field


class MySQLConfig(BaseSettings):
    '''MySQL config

    Attributes:
        host (str): database host
        port (int): database port
        user (str): database username
        password (str): database password
        database (str): database name
    '''
    host: str
    port: int = Field(3306)
    user: str
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
    broker_url: str = Field(alias='broker')
    result_backend: str = Field(alias='backend')
    timezone: str = 'Asia/Taipei'
    task_serializer: str = 'json'
    result_backend_transport_options: typing.Dict = {
        'visibility_timeout': 3600,
    }
    installed_apps: typing.List = [
        'eyes.celery.crawler.tasks',
        'eyes.celery.stats.tasks',
    ]

    class Config:
        env_prefix = 'celery_'
