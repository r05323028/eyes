'''Crawler module integration test
'''
from typing import Dict, List

import pytest
import sqlalchemy as sa
from sqlalchemy.orm import sessionmaker

from eyes.tasks import crawl_ptt_post, crawl_ptt_posts
from eyes.config import DatabaseConfig


class TestCrawler:
    '''Crawler module integration test cases
    '''
    @pytest.fixture
    def tables(self):
        yield ['ptt_posts', 'ptt_comments']

    @pytest.fixture
    def session(self, tables):
        db_config = DatabaseConfig()
        engine = sa.create_engine(
            f'mysql://{db_config.username}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}?charset=utf8mb4'
        )
        session = sessionmaker(engine)()
        session.execute('SET FOREIGN_KEY_CHECKS=0')
        session.commit()
        for tbl in tables:
            session.execute(f'TRUNCATE TABLE {tbl}')
        session.commit()
        yield session
        for tbl in tables:
            session.execute(f'TRUNCATE TABLE {tbl}')
        session.commit()

    def test_ptt_celery_crawler(self, session):
        '''Test ptt celery crawler & orm model
        '''
        board = 'Gossiping'
        url = 'https://www.ptt.cc/bbs/Gossiping/M.1628066356.A.16F.html'
        res = crawl_ptt_post.delay(url, board)
        post = res.get()

        assert isinstance(post, Dict)

    def test_ptt_celery_bulk_crawler(self, session):
        '''Test ptt celery bulk insert
        '''
        board = 'Gossiping'
        urls = [
            'https://www.ptt.cc/bbs/Gossiping/M.1628179660.A.249.html',
            'https://www.ptt.cc/bbs/Gossiping/M.1628179746.A.DD9.html',
            'https://www.ptt.cc/bbs/Gossiping/M.1628179676.A.C1A.html',
        ]

        res = crawl_ptt_posts.delay(urls, board)
        posts = res.get()

        assert isinstance(posts, List)
        assert isinstance(posts[0], Dict)
