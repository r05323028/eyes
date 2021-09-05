'''API module
'''
import sqlalchemy as sa
from fastapi import FastAPI
from sqlalchemy.orm import scoped_session, sessionmaker
from starlette.graphql import GraphQLApp

from eyes.config import DatabaseConfig
from eyes.db import Base
from eyes.schema import schema


def create_app() -> FastAPI:
    '''Create FastAPI app

    Returns:
        FastAPI
    '''
    config = DatabaseConfig()
    engine = sa.create_engine(
        f'mysql://{config.user}:{config.password}@{config.host}:{config.port}/{config.database}?charset=utf8mb4'
    )
    sess = scoped_session(sessionmaker(engine))
    Base.bind = engine
    Base.query = sess.query_property()
    graphql_app = GraphQLApp(schema=schema)
    app = FastAPI()
    app.add_route('/', graphql_app)

    return app


app = create_app()
