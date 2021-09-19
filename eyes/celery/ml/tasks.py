'''Eyes celery ml tasks
'''
from datetime import datetime
from itertools import zip_longest
from typing import Dict

import spacy
import sqlalchemy as sa
from spacy.tokens import Doc
from sqlalchemy.orm import scoped_session, sessionmaker

from celery import Task
from celery.utils.log import get_task_logger
from eyes.celery import app
from eyes.config import MySQLConfig, SpacyConfig
from eyes.db.ptt import PttPost
from eyes.db.spacy import SpacyPttPost
from eyes.exception import PostNotExistsError
from eyes.ml.spacy import transform_ptt_post_to_spacy

logger = get_task_logger(__name__)


class MlTask(Task):
    '''Ml Base Task
    '''
    _sess = None
    _nlp = None

    @property
    def nlp(self):
        '''Returns spacy language model
        '''
        if self._nlp is None:
            config = SpacyConfig()
            nlp = spacy.load(config.name)
            self._nlp = nlp

        return self._nlp

    @property
    def sess(self):
        '''Returns SQLAlchemy Session
        '''
        if self._sess is None:
            db_config = MySQLConfig()
            engine = sa.create_engine(
                f'mysql://{db_config.user}:{db_config.password}@{db_config.host}:\
                    {db_config.port}/{db_config.database}?charset=utf8mb4')
            session_factory = sessionmaker(engine)
            self._sess = scoped_session(session_factory)()

        return self._sess


@app.task(
    bind=True,
    base=MlTask,
)
def transform_ptt_post_to_spacy_post(
    self,
    post_id: str,
) -> Dict:
    '''Transform ptt post to spacy post

    Args:
        post_id (str): ptt post id

    Returns:
        Dict: transformed post
    '''
    post = self.sess.query(PttPost).filter(PttPost.id == post_id).first()
    if not post:
        raise PostNotExistsError(f"Post: {post_id} is not exist")
    spacy_post = transform_ptt_post_to_spacy(post, self.nlp)
    exist_row = self.sess.query(SpacyPttPost).filter(
        SpacyPttPost.id == post_id).first()
    if exist_row:
        exist_row.title = spacy_post.title
        exist_row.content = spacy_post.content
        exist_row.updated_at = datetime.utcnow()
        new_comments = []
        for exist_comment, comment in zip_longest(
                sorted(exist_row.comments, key=lambda x: x.comment_id),
                sorted(spacy_post.comments, key=lambda x: x.comment_id),
        ):
            if exist_comment:
                exist_comment.content = comment.content
                exist_comment.updated_at = datetime.utcnow()
            else:
                new_comments.append(comment.to_orm())
        exist_row.comments.extend(new_comments)
        self.sess.merge(exist_row)
        self.sess.commit()
    else:
        row = spacy_post.to_orm()
        self.sess.add(row)
        self.sess.commit()

    return {
        'id': spacy_post.id,
        'title': Doc(self.nlp.vocab).from_bytes(spacy_post.title).text,
    }
