'''Eyes tasks
'''
import logging
import os
from typing import Dict

from celery import Celery, Task
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from eyes.config import DatabaseConfig
from eyes.crawler.ptt import crawl_post
from eyes.db import PttComment, PttPost

app = Celery(broker=os.environ.get('CELERY_BROKER_URL'),
             backend=os.environ.get('CELERY_RESULT_BACKEND'))
app.conf.timezone = 'Asia/Taipei'
app.conf.task_serializer = 'json'

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
            Session = sessionmaker(engine)

            self._sess = Session()

        return self._sess


@app.task(
    base=CrawlerTask,
    bind=True,
)
def crawl_ptt_post(
    self,
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
    row = post.dict()
    row['comments'] = [PttComment(**com) for com in row['comments']]
    row = PttPost(**row)
    self.sess.add(row)
    self.sess.commit()

    return post.dict()
