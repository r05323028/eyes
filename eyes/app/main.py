'''Eyes API entrypoint
'''
from fastapi import FastAPI

from eyes import __version__, APP_NAME
from eyes.app.routers import base


def create_app() -> FastAPI:
    '''Create API

    Returns:
        FastAPI
    '''
    api = FastAPI(
        title=APP_NAME,
        version=__version__,
    )

    api.include_router(base.router)

    return api


app = create_app()
