'''DB commands
'''
import logging

import click
import sqlalchemy as sa
from rich.logging import RichHandler
from sqlalchemy_utils.functions import create_database, database_exists

from eyes.db import Base

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(RichHandler(rich_tracebacks=True))


@click.group()
def db():
    '''Eyes DB Commands
    '''


@click.command()
@click.option(
    '--host',
    required=True,
    help='Database host',
    envvar="MYSQL_HOST",
)
@click.option(
    '--port',
    default=3306,
    help='Database port',
    envvar="MYSQL_PORT",
)
@click.option(
    '-u',
    '--user',
    required=True,
    help='Database user',
    envvar="MYSQL_USER",
)
@click.option(
    '-p',
    '--password',
    prompt=True,
    hide_input=True,
    help='Database password',
    envvar="MYSQL_PASSWORD",
)
@click.option(
    '--database',
    default='eyes',
    help='Database name',
    envvar="MYSQL_DATABASE",
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
    logger.info('Initialing database: %s ...', database)
    url = f'mysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4'
    engine = sa.create_engine(url, echo=True)

    if not database_exists(engine.url):
        logger.info('Database: %s not exists, creates it.', database)

        create_database(engine.url, encoding='utf8mb4')

    Base.metadata.create_all(bind=engine)


@click.command()
@click.option(
    '--host',
    required=True,
    help='Database host',
    envvar="MYSQL_HOST",
)
@click.option(
    '--port',
    default=3306,
    help='Database port',
    envvar="MYSQL_PORT",
)
@click.option(
    '-u',
    '--user',
    required=True,
    help='Database user',
    envvar="MYSQL_USER",
)
@click.option(
    '-p',
    '--password',
    prompt=True,
    hide_input=True,
    help='Database password',
    envvar="MYSQL_PASSWORD",
)
@click.option(
    '--database',
    default='eyes',
    help='Database name',
    envvar="MYSQL_DATABASE",
)
def drop_tables(
    host: str,
    port: int,
    user: str,
    password: str,
    database: str,
):
    '''Drop all tables in database
    '''
    url = f'mysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4'
    engine = sa.create_engine(url)
    Base.metadata.drop_all(bind=engine)


db.add_command(init)
db.add_command(drop_tables)
