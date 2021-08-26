'''Crawler module integration test
'''
from typing import Dict, List

import pytest
import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker

from eyes.config import DatabaseConfig
from eyes.tasks import (
    crawl_dcard_board_list,
    crawl_dcard_post,
    crawl_ptt_board_list,
    crawl_ptt_post,
    crawl_wiki_entity,
)


class TestCrawler:
    '''Crawler module integration test cases
    '''
    @pytest.fixture
    def tables(self):
        yield [
            'ptt_posts', 'ptt_comments', 'dcard_posts', 'dcard_comments',
            'dcard_reactions'
        ]

    @pytest.fixture
    def session(
        self,
        tables,
    ):
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
        session.close()

    def test_ptt_celery_crawler(
        self,
        session: Session,
    ):
        '''Test ptt celery crawler & orm model
        '''
        board = 'Gossiping'
        url = 'https://www.ptt.cc/bbs/Gossiping/M.1628066356.A.16F.html'
        res = crawl_ptt_post.delay(url, board)
        post = res.get()

        assert isinstance(post, Dict)

    def test_ptt_celery_board_list_crawler(
        self,
        session: Session,
    ):
        res = crawl_ptt_board_list.delay(top_n=5)
        board_list = res.get()

        assert isinstance(board_list, List)
        assert isinstance(board_list[0], Dict)

    def test_dcard_celery_crawler(
        self,
        session: Session,
    ):
        '''Test dcard celery post crawler
        '''
        post_id = 236766080
        res = crawl_dcard_post.delay(post_id)
        post = res.get()

        assert isinstance(post, Dict)

    def test_dcard_celery_board_list_cralwer(
        self,
        session: Session,
    ):
        res = crawl_dcard_board_list.delay(top_n=5)
        board_list = res.get()

        assert isinstance(board_list, List)
        assert isinstance(board_list[0], Dict)

    def test_wiki_celery_entity_crawler(
        self,
        session: Session,
    ):
        res = crawl_wiki_entity.delay(
            url='https://zh.wikipedia.org/wiki/%E5%BC%B5%E6%83%A0%E5%A6%B9')
        ent = res.get()

        assert isinstance(ent, Dict)
