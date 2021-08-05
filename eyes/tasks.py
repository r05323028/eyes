'''Eyes tasks
'''
import logging
import os
from typing import Dict

from celery import Celery

from eyes.crawler.ptt import crawl_post

app = Celery(broker=os.environ.get('CELERY_BROKER_URL'),
             backend=os.environ.get('CELERY_RESULT_BACKEND'))
app.conf.timezone = 'Asia/Taipei'
app.conf.task_serializer = 'json'

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


@app.task
def crawl_ptt_post(
    url: str,
    board: str,
) -> Dict:
    '''Crawl a ptt post and store it into database

    Args:
        url (str): post url
        board (str): board name

    Returns:
        Dict: post dictionary
    '''
    post = crawl_post(url, board)

    return post.dict()
