'''Eyes celery tasks
'''
import logging
import os
from datetime import datetime
from itertools import zip_longest
from typing import Dict, List, Optional

import sqlalchemy as sa
from celery import Celery, Task
from sqlalchemy.orm import sessionmaker

from eyes.config import DatabaseConfig
from eyes.crawler.ptt import crawl_board_list, crawl_post
from eyes.db import PttBoard, PttComment, PttPost

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

    exist_row = self.sess.query(PttPost).filter(PttPost.id == post.id).first()

    if exist_row:
        exist_row.author = post.author
        exist_row.title = post.title
        exist_row.content = post.content

        # upsert comments
        new_comments = []
        for exist_comment, crawled_comment in zip_longest(
                sorted(exist_row.comments, key=lambda x: x.comment_id),
                sorted(post.comments, key=lambda x: x.comment_id)):
            if exist_comment:
                exist_comment.reaction = crawled_comment.reaction
                exist_comment.author = crawled_comment.author
                exist_comment.content = crawled_comment.content
                exist_comment.updated_at = datetime.utcnow()
            else:
                new_comments.append(PttComment(**crawled_comment.dict()))
        exist_row.comments.extend(new_comments)
        exist_row.updated_at = datetime.utcnow()
        self.sess.merge(exist_row)
        self.sess.commit()
    else:
        row = post.dict()
        row['comments'] = [
            PttComment(
                comment_id=com['comment_id'],
                post_id=com['post_id'],
                reaction=com['reaction'],
                author=com['author'],
                content=com['content'],
                created_at=com['created_at'],
                updated_at=datetime.utcnow(),
            ) for com in row['comments']
        ]
        row = PttPost(**row)

        self.sess.add(row)
        self.sess.commit()

    return post.dict()


@app.task(base=CrawlerTask, bind=True)
def crawl_ptt_board_list(
    self,
    top_n: Optional[int] = None,
) -> Optional[List[Dict]]:
    '''Crawl ptt board list
    '''
    ret = []
    boards = crawl_board_list(top_n)

    for board in boards:
        exist_board = self.sess.query(PttBoard).filter(
            PttBoard.name == board.name).first()

        if exist_board:
            exist_board.name = board.name
            exist_board.url = board.url
            exist_board.updated_at = datetime.utcnow()
            self.sess.merge(exist_board)
            self.sess.commit()

        else:
            new_board = PttBoard(**board.dict())
            self.sess.add(new_board)
            self.sess.commit()

        ret.append(board.dict())

    return ret
