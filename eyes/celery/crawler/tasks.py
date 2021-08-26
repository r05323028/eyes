'''Eyes celery tasks
'''
import logging
from datetime import datetime
from itertools import zip_longest
from typing import Dict, List, Optional

import sqlalchemy as sa
from celery import Task
from sqlalchemy.orm import sessionmaker

from eyes.celery import app
from eyes.config import DatabaseConfig
from eyes.crawler import ptt, dcard, entity
from eyes.db import PttBoard, PttPost, DcardPost, DcardComment, DcardBoard, WikiEntity

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


class CrawlerTask(Task):
    '''Crawler Base Task
    '''
    _sess = None

    def after_return(self, *args, **kwargs):
        '''Callback after finishing a job
        '''
        if self._sess is not None:
            self._sess.close()

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
    post = ptt.crawl_post(url, board)

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
                new_comments.append(crawled_comment.to_orm())
        exist_row.comments.extend(new_comments)
        exist_row.updated_at = datetime.utcnow()
        self.sess.merge(exist_row)
        self.sess.commit()
    else:
        self.sess.add(post.to_orm())
        self.sess.commit()

    return post.dict()


@app.task(
    base=CrawlerTask,
    bind=True,
)
def crawl_ptt_board_list(
    self,
    top_n: Optional[int] = None,
) -> Optional[List[Dict]]:
    '''Crawl ptt board list

    Args:
        top_n (Optional[int]): top N boards

    Returns:
        Optional[List[Dict]]
    '''
    ret = []
    boards = ptt.crawl_board_list(top_n)

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
            self.sess.add(board.to_orm())
            self.sess.commit()

        ret.append(board.dict())

    return ret


@app.task(
    base=CrawlerTask,
    bind=True,
)
def crawl_dcard_post(
    self,
    post_id: int,
) -> Optional[Dict]:
    '''Crawl dcard post

    Args:
        post_id (int): post id

    Returns:
        Optional[Dict]: post dictionary
    '''
    post = dcard.crawl_post(post_id)

    if not post:
        return

    exist_row = self.sess.query(DcardPost).filter(
        DcardPost.id == post.id).first()

    if exist_row:
        exist_row.title = post.title
        exist_row.content = post.content
        exist_row.school = post.school
        exist_row.gender = post.gender
        exist_row.topics = post.topics
        exist_row.like_count = post.like_count
        exist_row.with_nickname = post.with_nickname
        exist_row.anonymous_school = post.anonymous_school
        exist_row.anonymous_department = post.anonymous_department
        exist_row.media = post.media

        # reactions
        new_reactions = []
        for exist_reaction, crawled_reaction in zip_longest(
                sorted(exist_row.reactions, key=lambda x: x.reaction_id),
                sorted(post.reactions, key=lambda x: x.reaction_id),
        ):
            if exist_reaction:
                exist_reaction.count = crawled_reaction.count
            else:
                new_reactions.append(crawled_reaction.to_orm())
            exist_row.reactions.extend(new_reactions)

        # comments
        new_comments = []
        for exist_comment, crawled_comment in zip_longest(
                sorted(exist_row.comments, key=lambda x: x.floor),
                sorted(post.comments, key=lambda x: x.floor),
        ):
            if exist_comment:
                exist_comment.anonymous = crawled_comment.anonymous
                exist_comment.with_nickname = crawled_comment.with_nickname
                exist_comment.content = crawled_comment.content
                exist_comment.gender = crawled_comment.gender
                exist_comment.school = crawled_comment.school
                exist_comment.host = crawled_comment.host
                exist_comment.like_count = crawled_comment.like_count
                exist_comment.updated_at = crawled_comment.updated_at
            else:
                new_comments.append(DcardComment(**crawled_comment.dict()))
        exist_row.comments.extend(new_comments)

        self.sess.merge(exist_row)
        self.sess.commit()
    else:
        self.sess.add(post.to_orm())
        self.sess.commit()

    return post.dict()


@app.task(
    base=CrawlerTask,
    bind=True,
)
def crawl_dcard_board_list(
    self,
    top_n: Optional[int] = None,
) -> Optional[List[Dict]]:
    '''Crawl dcard board list

    Args:
        top_n (Optional[int]): top N boards

    Returns:
        Optional[List[Dict]]
    '''
    ret = []
    boards = dcard.crawl_board_list(top_n)

    for board in boards:
        exist_board = self.sess.query(DcardBoard).filter(
            DcardBoard.id == board.id).first()

        if exist_board:
            exist_board.name = board.name
            exist_board.alias = board.alias
            exist_board.description = board.description
            exist_board.is_school = board.is_school
            self.sess.merge(exist_board)
            self.sess.commit()
        else:
            self.sess.add(board.to_orm())
            self.sess.commit()

        ret.append(board.dict())

    return ret


@app.task(
    base=CrawlerTask,
    bind=True,
)
def crawl_wiki_entity(
    self,
    url: str,
) -> Optional[Dict]:
    '''Crawl wiki entity

    Args:
        url (str): entity url

    Returns:
        Optional[Dict]: wiki entity dictionary
    '''
    crawled_entity = entity.crawl_wiki_entity(url)
    exist_entity = self.sess.query(WikiEntity).filter(
        WikiEntity.name == crawled_entity.name).first()
    if exist_entity:
        exist_entity.alias = crawled_entity.alias
        exist_entity.type = crawled_entity.type
        self.sess.merge(exist_entity)
        self.sess.commit()
    else:
        self.sess.add(crawled_entity.to_wiki_entity_orm())
        self.sess.commit()

    return crawled_entity.dict()
