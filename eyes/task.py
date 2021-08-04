'''Eyes tasks
'''
from celery import Celery

from eyes.crawler import Crawler

app = Celery()


@app.task
def crawl_latest_posts(crawler: Crawler):
    '''Crawl latest posts

    Args:
        crawler (Crawler): Crawler instance
    '''
    ...
