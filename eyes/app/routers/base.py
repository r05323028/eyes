'''Eyes API base router
'''
from datetime import datetime

from fastapi import APIRouter

from eyes import __version__, APP_NAME

router = APIRouter()


@router.get('/health')
def health():
    '''Health check route
    '''
    return {
        'name': APP_NAME,
        'version': __version__,
        'datetime': datetime.utcnow(),
    }
