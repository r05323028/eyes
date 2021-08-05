'''Crawler module integration test
'''
from typing import Dict

import sqlalchemy as sa
from sqlalchemy.orm import Session

from eyes.config import DatabaseConfig
from eyes.db import PttComment, PttPost
from eyes.tasks import crawl_ptt_post


class TestCrawler:
    '''Crawler module integration test cases
    '''
    def test_ptt_celery_crawler(self):
        '''Test ptt celery crawler & orm model
        '''
        board = 'Gossiping'
        url = 'https://www.ptt.cc/bbs/Gossiping/M.1628066356.A.16F.html'
        res = crawl_ptt_post.delay(url, board)
        post = res.get()

        assert isinstance(post, Dict)

        db_config = DatabaseConfig()

        engine = sa.create_engine(
            f'mysql://{db_config.username}:{db_config.password}@{db_config.host}:\
                {db_config.port}/{db_config.database}?charset=utf8mb4')

        with Session(engine) as sess:
            post['comments'] = [PttComment(**com) for com in post['comments']]
            row = PttPost(**post)
            sess.add(row)
            sess.commit()
