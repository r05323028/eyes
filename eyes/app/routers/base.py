'''API base router
'''
from fastapi import APIRouter

from eyes import __version__

router = APIRouter()


@router.get('/health')
def health():
    '''Health check
    '''
    return {
        'name': "Eyes",
        'version': __version__,
    }
