'''Eyes commands
'''
import logging

import click
import sqlalchemy as sa
from sqlalchemy.engine import create_engine
from sqlalchemy_utils.functions import create_database, database_exists

from eyes.db import Base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

CONTEXT_SETTINGS = {
    'help_option_names': ['-h', '--help'],
}


@click.group()
def db():
    '''Eyes DB Commands
    '''


@click.command()
@click.option(
    '--host',
    required=True,
    help='database host',
)
@click.option(
    '--port',
    default=3306,
    help='database port',
)
@click.option(
    '-u',
    '--user',
    required=True,
    help='database user',
)
@click.option(
    '-p',
    '--password',
    prompt=True,
    hide_input=True,
    help='database password',
)
@click.option(
    '--database',
    default='eyes',
    help='database name',
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
        create_database(engine.url)

    Base.metadata.create_all(bind=engine)


@click.group(context_settings=CONTEXT_SETTINGS)
def cli():
    '''Eyes Command Line Tools
    '''


db.add_command(init)

cli.add_command(db)
