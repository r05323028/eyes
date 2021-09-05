'''PTT crawler module
'''
import logging
import os
import re
from datetime import datetime, timedelta
from typing import Iterator, Optional

import requests
from lxml import etree
from rich.logging import RichHandler

from eyes.crawler.utils import get_dom
from eyes.data import PttBoard, PttComment, PttPost

PTT_BASE_URL = 'https://www.ptt.cc'
PTT_OVER_18_BOARDS = [
    'Gossiping',
    'sex',
]
PTT_CRAWLER_SETTINGS = {
    'n_expired_posts': 100,
}

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(RichHandler(rich_tracebacks=True))


def get_post_id(url: str, ) -> str:
    '''Get post id by url

    Args:
        url (str): post url

    Returns:
        str: post id
    '''
    return os.path.basename(url).replace('.html', '')


def crawl_post(
    url: str,
    board: str,
) -> Optional[PttPost]:
    '''Crawl a ptt post into a PttPost

    Args:
        url (str): a post url
        board (str): board name

    Returns:
        Optional[PttPost]: ptt post data container, None if 404
    '''
    logger.info('Crawl %s', url)
    cookies = {}

    if board in PTT_OVER_18_BOARDS:
        cookies.update({
            'over18': '1',
        })

    resp = requests.get(url, cookies=cookies)

    if resp.status_code == 404:
        return

    dom = get_dom(resp)

    try:
        # article meta
        post_id = get_post_id(resp.url)

        author = ''.join(
            dom.xpath('//*[@id="main-content"]/div[1]/span[2]/text()'))

        board = ''.join(
            dom.xpath('//*[@id="main-content"]/div[2]/span[2]/text()'))
        title = ''.join(
            dom.xpath('//*[@id="main-content"]/div[3]/span[2]/text()'))
        post_created_at = ''.join(
            dom.xpath('//*[@id="main-content"]/div[4]/span[2]/text()'))
        if post_created_at:
            post_created_at = datetime.strptime(
                post_created_at,
                '%a %b  %d %H:%M:%S %Y',
            )
        else:
            post_created_at = datetime.utcfromtimestamp(0)

        # content
        content = dom.xpath('//*[@id="main-content"]/text()')
        content = ''.join(content)

        # comments
        comments = []
        comments_etree = dom.xpath('//div[@class="push"]')

        for com_id, com in enumerate(comments_etree):
            span = com.xpath('span')
            comment_created_at = re.findall(
                '[0-9]{2}/[0-9]{2} [0-9]{2}:[0-9]{2}', span[3].text)[0]
            comment_created_at = datetime.strptime(
                comment_created_at,
                '%m/%d %H:%M',
            )
            comment_created_at = comment_created_at.replace(
                year=datetime.now().year)

            comments.append(
                PttComment(
                    comment_id=com_id,
                    post_id=post_id,
                    reaction=span[0].text.strip(),
                    author=span[1].text,
                    content=span[2].text[2:],
                    created_at=comment_created_at,
                ))

        # post
        return PttPost(
            id=post_id,
            title=title,
            author=author,
            board=board,
            content=content,
            comments=comments,
            created_at=post_created_at,
            url=resp.url,
        )
    except IndexError:
        logger.error("Could not crawl %s", url)
        return


def get_next_url(dom: etree.Element) -> str:
    '''Get next page url

    Args:
        dom (etree.Element): current page DOM

    Returns:
        str: next page url
    '''
    return dom.xpath(
        '//*[@id="action-bar-container"]/div/div[2]/a[2]/@href')[0]


def crawl_post_urls(
    board: str,
    n_days: Optional[int] = None,
) -> Iterator[str]:
    '''Crawl latest N post urls

    Args:
        board (str): board name
        n_days (Optional[int]): number of days which posts are created at this range. If `n_days` is None, crawler will ignore this setting.

    Returns:
        Iterator[str]: a list of ptt post urls
    '''
    # expired settings
    if n_days:
        expired_counter = 0
        now = datetime.utcnow()
        critical_point = now - timedelta(days=n_days)

    cookies = {}

    if board in PTT_OVER_18_BOARDS:
        cookies.update({'over18': '1'})

    next_url = f'{PTT_BASE_URL}/bbs/{board}/index.html'
    resp = requests.get(next_url, cookies=cookies)
    dom = get_dom(resp)

    while next_url:
        # get post urls
        logger.info('Page: %s', next_url)
        r_ents = dom.xpath('//*[@class="r-ent"]')

        for row in r_ents:
            href = row.xpath('div[@class="title"]/a/@href')

            if href:
                post_url = f'{PTT_BASE_URL}{href[0]}'

                # check if post is expired
                if n_days:
                    created_at = row.xpath(
                        'div[@class="meta"]/div[@class="date"]/text()')[0]
                    created_at = datetime.strptime(created_at.strip(), '%m/%d')
                    created_at = created_at.replace(
                        year=now.
                        year if created_at.month <= now.month else now.year -
                        1)

                    if created_at < critical_point:
                        logger.info(
                            "Catch an expired post %s (created at: %s)",
                            post_url,
                            created_at.strftime("%Y-%m-%d"),
                        )
                        expired_counter += 1

                yield post_url

        # terminate loop if expired_posts exceeds limitation
        if n_days and expired_counter > PTT_CRAWLER_SETTINGS['n_expired_posts']:
            logger.info("n_expired_posts exceeds limitation: %s",
                        expired_counter)
            break

        next_url = get_next_url(dom)
        resp = requests.get(f'{PTT_BASE_URL}{next_url}', cookies=cookies)
        dom = get_dom(resp)


def crawl_board_list(top_n: Optional[int] = None) -> Iterator[PttBoard]:
    '''Crawl PTT post

    Args:
        top_n (int): top N boards.

    Returns:
        Iterator[PttBoard]
    '''
    board_url = f'{PTT_BASE_URL}/bbs/hotboards.html'
    resp = requests.get(board_url)
    dom = get_dom(resp)
    logger.info('Crawl PTT board list')

    for i, board in enumerate(dom.xpath('//*[@class="b-ent"]')):
        name = ''.join(board.xpath('a/div[@class="board-name"]/text()'))
        url = ''.join(board.xpath('a/@href'))
        url = f'{PTT_BASE_URL}{url}'

        yield PttBoard(
            name=name,
            url=url,
        )

        if top_n and i > top_n:
            break
