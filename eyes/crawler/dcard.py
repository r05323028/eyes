'''Dcard Crawler module
'''
import logging
from datetime import datetime
from typing import Iterator, Optional

import requests
from fake_useragent import UserAgent
from requests.models import HTTPError
from rich.logging import RichHandler

from eyes.data.dcard import DcardBoard, DcardComment, DcardPost, DcardReaction

ISO_FORMAT = '%Y-%m-%dT%H:%M:%S.%fZ'

DCARD_BASE_URL = 'https://www.dcard.tw/_api'

logger = logging.getLogger(__name__)
logger.addHandler(RichHandler(rich_tracebacks=True))
ua = UserAgent()
headers = {
    'User-Agent': ua.random,
}


def crawl_post(post_id: int) -> DcardPost:
    '''Crawl a dcard post

    Args:
        post_id (int): post id

    Returns:
        DcardPost: dcard post
    '''
    url = f'{DCARD_BASE_URL}/posts/{post_id}'

    # crawl comments
    comment_resp = requests.get(
        f'{url}/comments',
        headers=headers,
    )
    comments = [
        DcardComment(
            id=com['id'],
            post_id=com['postId'],
            anonymous=com['anonymous'],
            with_nickname=com['withNickname'],
            floor=com['floor'],
            content=com['content'],
            gender=com['gender'],
            school=com['school'],
            host=com['host'],
            like_count=com['likeCount'],
            created_at=datetime.strptime(com['createdAt'], ISO_FORMAT),
            updated_at=datetime.strptime(com['updatedAt'], ISO_FORMAT),
        ) for com in comment_resp.json()
    ]

    # crawl post
    resp = requests.get(
        url,
        headers=headers,
    )
    if resp.status_code == 404:
        raise HTTPError(
            'Could not fetch %s',
            post_id,
        )

    data = resp.json()

    return DcardPost(
        id=data['id'],
        forum_id=data['forumId'],
        forum_name=data['forumName'],
        title=data['title'],
        content=data['content'],
        school=data.get('school', None),
        gender=data['gender'],
        topics=data['topics'],
        like_count=data['likeCount'],
        reactions=[
            DcardReaction(
                reaction_id=react['id'],
                count=react['count'],
                post_id=data['id'],
            ) for react in data['reactions']
        ],
        with_nickname=data['withNickname'],
        anonymous_school=data['anonymousSchool'],
        anonymous_department=data['anonymousDepartment'],
        media=data['media'],
        comments=comments,
        created_at=datetime.strptime(data['createdAt'], ISO_FORMAT),
        updated_at=datetime.strptime(data['updatedAt'], ISO_FORMAT),
    )


def crawl_post_ids(
    forum_id: str,
    n_days: int = None,
) -> Iterator[int]:
    '''Crawl dcard post ids

    Args:
        forum_id (str): forum id
        n_days (str): number of days which posts are created at this range. If `n_days` is None, crawler will ignore this setting.

    Returns:
        Iterator[int]: post id iterator
    '''
    url = f'{DCARD_BASE_URL}/forums/{forum_id}/posts'
    resp = requests.get(
        url,
        headers=headers,
    )
    data = resp.json()

    for post in data:
        yield post['id']


def crawl_board_list(top_n: Optional[int] = None) -> Iterator[DcardBoard]:
    '''Crawl Dcard forum list

    Args:
        top_n (Optional[int]): max number of boards

    Returns:
        Iterator[DcardBoard]: board iterator
    '''
    url = f'{DCARD_BASE_URL}/forums'
    resp = requests.get(
        url,
        headers=headers,
    )
    logger.info('Crawl dcard board list')

    for i, board in enumerate(resp.json()):
        created_at = datetime.strptime(board['createdAt'], ISO_FORMAT)
        updated_at = datetime.strptime(board['updatedAt'], ISO_FORMAT)

        yield DcardBoard(
            id=board['id'],
            name=board['name'],
            alias=board['alias'],
            description=board['description'],
            is_school=board['isSchool'],
            created_at=created_at,
            updated_at=updated_at,
        )

        if top_n and i > top_n:
            break
