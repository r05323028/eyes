'''DB commands
'''
import logging

import click
import sqlalchemy as sa
from sqlalchemy.orm import Session
from sqlalchemy_utils.functions import create_database, database_exists

from eyes.db import Base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@click.group()
def db():
    '''Eyes DB Commands
    '''


@click.command()
@click.option(
    '--host',
    required=True,
    help='Database host',
)
@click.option(
    '--port',
    default=3306,
    help='Database port',
)
@click.option(
    '-u',
    '--user',
    required=True,
    help='Database user',
)
@click.option(
    '-p',
    '--password',
    prompt=True,
    hide_input=True,
    help='Database password',
)
@click.option(
    '--database',
    default='eyes',
    help='Database name',
)
def init(
    host: str,
    port: int,
    user: str,
    password: str,
    database: str,
):
    '''Databases initialization
    '''
    url = f'mysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4'
    engine = sa.create_engine(url)

    if not database_exists(engine.url):
        logger.info('Database: %s not exists, creates it.', database)

        create_database(engine.url, encoding='utf8mb4')

    Base.metadata.create_all(bind=engine)


db.add_command(init)
