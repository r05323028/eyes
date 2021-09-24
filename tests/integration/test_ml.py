'''Ml module integration test
'''
from typing import Dict

import pytest
import spacy
import sqlalchemy as sa
from spacy.language import Language
from spacy.tokens import Doc
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from eyes.config import MySQLConfig, SpacyConfig
from eyes.data import spacy as spacy_data
from eyes.db import ptt
from eyes.db import spacy as spacy_db
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

    def test_transform_spacy_ptt_post_to_dict(
        self,
        nlp: Language,
        session: Session,
    ):
        '''Test transform spacy ptt post to dict
        '''
        row = session.query(spacy_db.SpacyPttPost).first()
        data = spacy_data.SpacyPttPost.from_orm(row)
        result = spacy_ml.transform_ptt_post(data, nlp)

        assert isinstance(result, Dict)
        assert isinstance(result['content'], Doc)
        for comment in result['comments']:
            assert isinstance(comment['content'], Doc)
