'''Train commands
'''
import click
import spacy
import sqlalchemy as sa
from spacy.tokens import DocBin
from sqlalchemy.orm import scoped_session, sessionmaker

from eyes.ml.spacy import build_docs


@click.group()
def train():
    '''Eyes Train Commands
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
@click.option(
    '--model',
    default='zh_core_web_md',
    help="Spacy model name",
)
@click.option(
    '--limit',
    default=10000,
    type=int,
    help="Max number of docs",
)
@click.option(
    '--batch_size',
    default=32,
    type=int,
    help="Batch size",
)
@click.argument('filename')
def build_dataset(
    host: str,
    port: int,
    user: str,
    password: str,
    database: str,
    model: str,
    limit: int,
    batch_size: int,
    filename: str,
):
    '''Build Dataset
    '''
    engine = sa.create_engine(
        f'mysql://{user}:{password}@{host}:{port}/{database}?charset=utf8mb4')
    Session = scoped_session(sessionmaker(engine))
    sess = Session()
    nlp = spacy.load(model)
    docs = build_docs(
        nlp,
        sess,
        limit,
        batch_size,
    )
    docbin = DocBin()
    for doc in docs:
        docbin.add(doc)
    docbin.to_disk(filename)


train.add_command(build_dataset)
