'''Tests of Crawler module
'''
from eyes.crawler import PttCrawler
from eyes.data import PttPost


class TestCrawler:
    '''Crawler module test cases
    '''
    def test_ptt_crawler(self):
        '''Test ptt crawler
        '''
        crawler = PttCrawler(board='Gossiping')

        url = 'https://www.ptt.cc/bbs/Gossiping/M.1628066356.A.16F.html'
        post = crawler.crawl_post(url)

        assert isinstance(post, PttPost)
