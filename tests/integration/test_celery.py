'''Crawler module integration test
'''
from typing import Dict, List

import pytest
import sqlalchemy as sa
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from eyes.celery.crawler.tasks import (
    crawl_dcard_board_list,
    crawl_dcard_post,
    crawl_ptt_board_list,
    crawl_ptt_post,
    crawl_wiki_entity,
)
from eyes.celery.ml.tasks import transform_ptt_post_to_spacy_post
from eyes.celery.stats.tasks import ptt_monthly_summary
from eyes.config import MySQLConfig
from eyes.db.ptt import PttPost


class TestCrawler:
    '''Crawler module integration test cases
    '''
    @pytest.fixture
    def tables(self):
        yield [
            'ptt_posts',
            'ptt_comments',
            'ptt_boards',
            'dcard_posts',
            'dcard_comments',
            'dcard_reactions',
            'dcard_boards',
            'wiki_entities',
        ]

    @pytest.fixture
    def session(self):
        db_config = MySQLConfig()
        engine = sa.create_engine(
            f'mysql://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}?charset=utf8mb4'
        )
        session_factory = sessionmaker(engine)
        session = scoped_session(session_factory)()
        yield session
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


class TestStats:
    '''Stats module integration test cases
    '''
    @pytest.fixture
    def tables(self):
        yield [
            'stats_monthly_summaries',
        ]

    @pytest.fixture
    def session(
        self,
        tables,
    ):
        db_config = MySQLConfig()
        engine = sa.create_engine(
            f'mysql://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}?charset=utf8mb4'
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

    def test_ptt_celery_stats(
        self,
        session: Session,
    ):
        year = 2021
        month = 9
        res = ptt_monthly_summary.delay(year, month)
        stat = res.get()

        assert isinstance(stat['total_posts'], int)
        assert isinstance(stat['total_comments'], int)


class TestMl:
    '''Ml module integration test cases
    '''
    @pytest.fixture
    def session(self):
        db_config = MySQLConfig()
        engine = sa.create_engine(
            f'mysql://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}?charset=utf8mb4'
        )
        session_factory = sessionmaker(engine)
        session = scoped_session(session_factory)()
        yield session
        session.close()

    def test_celery_transform_ptt_post_to_spacy(
        self,
        session: Session,
    ):
        '''Test celery transform ptt post to spacy
        '''
        post = session.query(PttPost).first()
        res = transform_ptt_post_to_spacy_post.delay(post.id)

        post_transformed = res.get()

        assert isinstance(post_transformed['id'], str)
        assert isinstance(post_transformed['title'], str)
