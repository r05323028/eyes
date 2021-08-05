'''Tests of Crawler module
'''
import os
import re

from eyes.crawler.ptt import crawl_post, crawl_post_urls
from eyes.data import PttPost


class TestPttCrawler:
    '''PttCrawler test cases
    '''
    def test_crawl_post(self):
        '''Test ptt crawl post
        '''
        url = 'https://www.ptt.cc/bbs/Gossiping/M.1628066356.A.16F.html'
        post = crawl_post(url, 'Gossiping')

        assert isinstance(post, PttPost)

    def test_crawl_post_urls(self):
        '''Test ptt crawl post urls
        '''
        posts = []
        post_urls = crawl_post_urls(board='Gossiping')

        for i, post in enumerate(post_urls):
            posts.append(post)

            if i > 100:
                break

        for post in posts:
            assert re.match('[A-Z].[0-9]{10}.[A-Z].[A-Z0-9]{3}.html',
                            os.path.basename(post))


class TestDcardCrawler:
    '''DcardCrawler test cases
    '''
