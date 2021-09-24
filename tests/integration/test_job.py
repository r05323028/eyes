'''Test job module
'''
import pytest
import sqlalchemy as sa
from sqlalchemy.orm import Session, sessionmaker

from eyes.config import MySQLConfig
from eyes.job import Job, Jobs, JobType


class TestJob:
    '''Eyes job test cases
    '''
    @pytest.fixture
    def session(
        self,
    ):
        db_config = MySQLConfig()
        engine = sa.create_engine(
            f'mysql://{db_config.user}:{db_config.password}@{db_config.host}:{db_config.port}/{db_config.database}?charset=utf8mb4'
        )
        session = sessionmaker(engine)()
        yield session
        session.close()

    @pytest.mark.slow
    def test_dispatch(
        self,
        session: Session,
    ):
        '''Test job dispatch
        '''
        job = Job(
            job_type=JobType.CRAWL_PTT_LATEST_POSTS,
            payload={
                'n_days': 1,
                'board': 'sex',
            },
        )
        jobs = Jobs()
        jobs.dispatch(job)
