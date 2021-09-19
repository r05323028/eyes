'''Eyes config
'''
import pathlib
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
        timezone (str): celery timezone
        task_serializer (str): celery task serializer
        result_backend_transport_options (Dict): result backend transport options
        installed_apps (List): celery installed apps
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
        'eyes.celery.ml.tasks',
    ]

    class Config:
        env_prefix = 'celery_'


class SpacyConfig(BaseSettings):
    '''Spacy config

    Attributes:
        name (Union[str, Path]): spacy model name or path
    '''
    name: typing.Union[str, pathlib.Path] = 'zh_core_web_sm'

    class Config:
        env_prefix = 'spacy_'
