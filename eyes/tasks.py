'''Eyes celery tasks
'''
import logging
import os
from datetime import datetime
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

    exist_row = self.sess.query(PttPost).filter(PttPost.id == row.id).first()

    # upsert
    if exist_row:
        row.updated_at = datetime.utcnow()
        self.sess.merge(row)
    else:
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
    posts = {}

    for url in urls:
        post = crawl_post(url, board)

        if post:
            posts[post.id] = post

    exist_posts = []

    # update exist rows
    for exist_row in self.sess.query(PttPost).filter(
            PttPost.id.in_(posts.keys())).all():
        exist_post = posts.pop(exist_row.id)
        exist_posts.append(exist_post)

        # convert data container to orm model
        exist_post = exist_post.dict()
        exist_post['comments'] = [
            PttComment(**com) for com in exist_post['comments']
        ]
        exist_post = PttPost(**exist_post)
        exist_post.updated_at = datetime.utcnow()
        self.sess.merge(exist_post)

    new_rows = []

    # insert new rows
    for new_row in posts.values():
        new_row = new_row.dict()
        new_row['comments'] = [
            PttComment(**com) for com in new_row['comments']
        ]
        new_row = PttPost(**new_row)
        new_rows.append(new_row)

    self.sess.bulk_save_objects(new_rows)
    self.sess.commit()

    return [post.dict() for post in exist_posts + list(posts.values())]
