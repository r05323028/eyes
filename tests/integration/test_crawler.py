'''Crawler module integration test
'''
from typing import Dict

from eyes.tasks import crawl_ptt_post


class TestCrawler:
    '''Crawler module integration test cases
    '''
    def test_ptt_celery_crawler(self):
        '''Test ptt celery crawler & orm model
        '''
        board = 'Gossiping'
        url = 'https://www.ptt.cc/bbs/Gossiping/M.1628066356.A.16F.html'
        res = crawl_ptt_post.delay(url, board)
        post = res.get()

        assert isinstance(post, Dict)
