'''Ml module integration test
'''
import pytest
import spacy
import sqlalchemy as sa
from spacy.language import Language
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from eyes.config import MySQLConfig, SpacyConfig
from eyes.db import ptt
from eyes.ml import spacy as spacy_ml


class TestMl:
    '''Ml module integration test cases
    '''
    @pytest.fixture
    def nlp(self) -> Language:
        '''Spacy language model
        '''
        config = SpacyConfig()
        yield spacy.load(config.name)

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

    def test_transform_ptt_post_to_spacy(
        self,
        nlp: Language,
        session: Session,
    ):
        '''Test transform ptt post to spacy
        '''
        post = session.query(ptt.PttPost).first()
        post_transformed = spacy_ml.transform_ptt_post_to_spacy(post, nlp)

        assert isinstance(post_transformed.title, bytes)
        assert isinstance(post_transformed.content, bytes)
        for comment in post_transformed.comments:
            assert isinstance(comment.content, bytes)
