'''API module
'''
import sqlalchemy as sa
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import scoped_session, sessionmaker
from starlette.graphql import GraphQLApp

from eyes import __version__
from eyes.app.routers import base
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
    origins = ['*']
    sess = scoped_session(sessionmaker(engine))
    Base.bind = engine
    Base.query = sess.query_property()
    graphql_app = GraphQLApp(schema=schema)
    app = FastAPI(
        title="Eyes API",
        description="Eyes public opinion mining system API.",
        version=__version__,
    )
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*'],
    )
    app.add_route('/graphql', graphql_app)
    app.include_router(base.router)

    return app


app = create_app()
