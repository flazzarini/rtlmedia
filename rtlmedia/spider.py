import logging
from re import search
from bs4 import BeautifulSoup
from json import loads
from functools import lru_cache

from items import Page, Item
from fetcher import Fetcher

LOG = logging.getLogger(__name__)


class Spider(object):
    def __init__(self, fetcher=Fetcher(), items=10):
        self.fetcher = fetcher
        self.items = items

    @lru_cache(maxsize=10)
    def get_page_items(self, page, query="Journal"):
        """
        Returns all items from a page
        """
        content = self.fetcher.get_index_page(page)
        page_items = self._get_page_items(content, looking_for=query)
        return page_items

    def get_items(self, query="Journal"):
        result = []
        page_nr = 1
        while len(result) < self.items:
            page_items = self.get_page_items(page_nr, query=query)
            for page_item in page_items:
                content = self.fetcher.get_content(page_item.path)
                jitem = self._get_journal_item(content)
                result.append(jitem)
            page_nr += 1
        return result

    def _get_page_items(self, content, looking_for="Journal"):
        result = []
        bs = BeautifulSoup(content, "html.parser")
        listing = bs.find('ul', {'class': 'listing'})
        for li in listing.find_all('li'):
            path = li.find('a', href=True)
            title = li.find('span', {'class': 'item-title'})
            date = li.find('div', {'class': 'sub'}).find('a')
            if title.text == looking_for:
                page = Page(title.text, path['href'], date.text)
                LOG.info(
                    "Found Item {x.title} - {x.date} - {x.path}"
                    .format(x=page))
                result.append(page)
        return result

    def _get_journal_item(self, content):
        bs = BeautifulSoup(content, "html.parser")
        section = bs.find('section', {'class': 'mainbar-right omega body'})
        title = section.find('h1')
        date = section.find('p', {'class': 'sub'})

        # Extract stream url
        script = bs.find('script', {'language': 'Javascript'})
        res = search("_conf.sources = '(.*)';", str(script))
        if not res:
            LOG.error(
                "Expected Javascript code not found, instead we found this {}"
                .format(script))
            pass
        sources = loads(res.groups()[0])
        hq_source = sources.get('httphq', {}).get('src', None)
        if not hq_source:
            LOG.error(
                "No HQ Source found, instead found this {}"
                .format(sources))
            pass
        return Item(title.text, hq_source, date.text)
