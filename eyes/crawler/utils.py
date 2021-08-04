import bs4
import requests
from lxml import etree


def get_dom(resp: requests.Response) -> etree.Element:
    '''Transform response to etree.Element

    Args:
        resp (requests.Response): response

    Returns:
        etree.Element: DOM
    '''
    soup = bs4.BeautifulSoup(resp.content, 'html.parser')
    dom = etree.HTML(str(soup))

    return dom
