'''Tests of Crawler module
'''
from eyes.crawler.ptt import crawl_post, crawl_latest_posts
from eyes.data import PttPost
from eyes.tasks import crawl_ptt_post


class TestPttCrawler:
    '''PttCrawler test cases
    '''
    def test_crawl_post(self):
        '''Test ptt crawler
        '''

        url = 'https://www.ptt.cc/bbs/Gossiping/M.1628066356.A.16F.html'
        post = crawl_post(url, 'Gossiping')

        assert isinstance(post, PttPost)

    def test_crawl_latest_posts(self):
        crawl_ptt_post.delay(
            'https://www.ptt.cc/bbs/Gossiping/M.1628094056.A.D63.html',
            'Gossiping',
        )


class TestDcardCrawler:
    '''DcardCrawler test cases
    '''
