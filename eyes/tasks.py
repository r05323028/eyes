'''Eyes tasks
'''
from celery import Celery
from eyes.crawler.ptt import crawl_post

app = Celery(broker='redis://redis:6379/0')


@app.task
def crawl_ptt_post(
    url: str,
    board: str,
):
    '''Crawl a ptt post and store it into database

    Args:
        url (str): post url
        board (str): board name
    '''
    post = crawl_post(url, board)
    ...
