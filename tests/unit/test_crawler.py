'''Tests of Crawler module
'''
import os
import re

from eyes.crawler import ptt, dcard
from eyes.data import PttBoard, PttPost, DcardBoard, DcardPost


class TestPttCrawler:
    '''PttCrawler test cases
    '''
    def test_crawl_post(self):
        '''Test ptt crawl post
        '''
        url = 'https://www.ptt.cc/bbs/Gossiping/M.1628066356.A.16F.html'
        post = ptt.crawl_post(url, 'Gossiping')

        assert isinstance(post, PttPost)

    def test_crawl_post_urls(self):
        '''Test ptt crawl post urls
        '''
        posts = []
        post_urls = ptt.crawl_post_urls(board='Gossiping')

        for i, post in enumerate(post_urls):
            posts.append(post)

            if i > 10:
                break

        for post in posts:
            assert re.match(
                '[A-Z].[0-9]{10}.[A-Z].[A-Z0-9]{3}.html',
                os.path.basename(post),
            )

    def test_crawl_latest_urls(self):
        '''Test ptt crawl latest n days post urls
        '''
        post_urls = ptt.crawl_post_urls(board='sex', n_days=1)
        post_urls = [post for post in post_urls]

        for post_url in post_urls:
            assert re.match(
                '[A-Z].[0-9]{10}.[A-Z].[A-Z0-9]{3}.html',
                os.path.basename(post_url),
            )

    def test_crawl_board_list(self):
        '''Test ptt crawl board list
        '''
        boards = ptt.crawl_board_list(top_n=5)
        boards = list(boards)

        assert isinstance(boards, list)
        assert isinstance(boards[0], PttBoard)


class TestDcardCrawler:
    '''DcardCrawler test cases
    '''
    def test_crawl_post(self):
        '''Test crawl dcard post
        '''
        post = dcard.crawl_post(236764049)

        assert isinstance(post, DcardPost)

    def test_crawl_post_ids(self):
        '''Test crawl post ids
        '''
        post_ids = dcard.crawl_post_ids('6eeeafb2-9dac-4d81-ae4b-ffecf0ad4444')
        post_ids = list(post_ids)

        assert isinstance(post_ids, list)

    def test_crawl_board_list(self):
        '''Test crawl dcard board list
        '''
        boards = dcard.crawl_board_list(top_n=5)
        boards = list(boards)

        assert isinstance(boards[0], DcardBoard)
        assert isinstance(boards, list)
