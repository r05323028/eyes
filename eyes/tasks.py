'''Eyes celery tasks
'''
import logging
import os
from typing import Dict, List, Optional

import sqlalchemy as sa
from celery import Celery, Task
from sqlalchemy.orm import sessionmaker

from eyes.config import DatabaseConfig
from eyes.crawler.ptt import crawl_post
from eyes.db import PttComment, PttPost

app = Celery(broker=os.environ.get('CELERY_BROKER_URL'),
             backend=os.environ.get('CELERY_RESULT_BACKEND'))
app.conf.timezone = 'Asia/Taipei'
app.conf.task_serializer = 'json'
app.conf.result_backend_transport_options = {
    'visibility_timeout': 3600,
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class CrawlerTask(Task):
    '''Crawler Base Task
    '''
    _sess = None

    @property
    def sess(self):
        '''Returns SQLAlchemy Session
        '''
        if self._sess is None:
            db_config = DatabaseConfig()
            engine = sa.create_engine(
                f'mysql://{db_config.username}:{db_config.password}@{db_config.host}:\
                    {db_config.port}/{db_config.database}?charset=utf8mb4')
            self._sess = sessionmaker(engine)()

        return self._sess


@app.task(
    base=CrawlerTask,
    bind=True,
)
def crawl_ptt_post(
    self,
    url: str,
    board: str,
) -> Optional[Dict]:
    '''Crawl a ptt post and store it into database

    Args:
        url (str): post url
        board (str): board name

    Returns:
        Optional[Dict]: post dictionary
    '''
    post = crawl_post(url, board)

    if not post:
        return

    row = post.dict()
    row['comments'] = [PttComment(**com) for com in row['comments']]
    row = PttPost(**row)
    self.sess.add(row)
    self.sess.commit()

    return post.dict()


@app.task(
    base=CrawlerTask,
    bind=True,
)
def crawl_ptt_posts(
    self,
    urls: List[str],
    board: str,
) -> List[Dict]:
    '''Crawl posts and perform bulk insert

    Args:
        urls (List[str]): list of urls
        board (str): board name

    Returns:
        List[Dict]: list of posts
    '''
    rows = []
    posts = []

    for url in urls:
        post = crawl_post(url, board)

        if post:
            posts.append(post)

    for row in posts:
        row = row.dict()
        row['comments'] = [PttComment(**com) for com in row['comments']]
        row = PttPost(**row)
        rows.append(row)

    self.sess.bulk_save_objects(rows)
    self.sess.commit()

    return [post.dict() for post in posts]
