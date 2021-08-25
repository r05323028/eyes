'''Eyes entity crawler module
'''
import logging
import re
from typing import Optional, Iterator

import requests

from eyes.crawler.utils import get_dom
from eyes.data import Entity

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

WIKI_BASE_URL = "https://zh.wikipedia.org"


def crawl_wiki_entity(url: str) -> Optional[Entity]:
    '''Crawl wiki entity

    Args:
        url (str): wiki entity url

    Returns:
        Optional[Entity]: entity
    '''
    resp = requests.get(url)
    if resp.status_code != 200:
        logger.warning(
            'Could not crawl entity: %s',
            url,
        )
    dom = get_dom(resp)
    name = ''.join(dom.xpath('//*[@id="firstHeading"]/text()'))
    if re.match('.+\(.+\)', name):
        name = re.sub('(?= ?\().+(?<=\))', '', name)
    nicknames = dom.xpath('//*[@class="nickname"]/text()')
    alias = []
    for alia in nicknames:
        alias.extend(alia.split('、'))

    return Entity(
        name=name,
        alias=alias,
    )


def crawl_wiki_entity_urls(category_url: str) -> Iterator[str]:
    '''Crawl wiki entity urls by category url

    Args:
        category_url (str): category_url

    Returns:
        Iterator[str]: category url iterator
    '''
    resp = requests.get(category_url)
    if resp.status_code != 200:
        return None
    dom = get_dom(resp)
    next_url = dom.xpath(
        '//*[@id="mw-pages"]/a[text()="下一页" or text()="下一頁"]/@href')
    if next_url:
        next_url = next_url[0]
    while next_url:
        logger.info(
            "Crawl entity urls: %s",
            next_url,
        )
        urls = dom.xpath('//*[@id="mw-pages"]/div/div/div/ul/li/a/@href')
        for url in urls:
            yield f'{WIKI_BASE_URL}{url}'
        next_url = dom.xpath(
            '//*[@id="mw-pages"]/a[text()="下一页" or text()="下一頁"]/@href')
        if not next_url:
            break
        next_url = next_url[0]
        resp = requests.get(f'{WIKI_BASE_URL}{next_url}')
        dom = get_dom(resp)
