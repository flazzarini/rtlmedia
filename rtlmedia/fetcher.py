import requests
import logging
from urllib.parse import ParseResult, urlparse, urlencode, urljoin
from exc import JournalException

LOG = logging.getLogger(__name__)


class Fetcher(object):
    """
    Class responsible to get contents of pages from the main `tele.rtl.lu` site

    :param req_lib: URL Lib to use (default: `requests`)
    """
    base_url = "http://tele.rtl.lu/emissiounen/de-journal"

    def __init__(self, req_lib=requests):
        self.req_lib = req_lib
        self.parsed_base_url = urlparse(self.base_url)

    def get(self, url):
        """
        Gets the content from a url

        :param url: URL to get the content from
        :type url: str

        :returns: Raw content of the URL
        :rtype: str
        """
        try:
            response = self.req_lib.get(url)
            return response.content
        except requests.RequestException as exc:
            raise JournalException(exc)

    def get_content(self, path):
        """
        A simple method to return the content of a subpage, this method
        will include the `base_url` defined in this class.

        :param path: Subpath
        :type path: str

        :returns: Content of the page
        :rtype: str
        """
        try:
            url = urljoin(self.base_url, path)
            response = self.req_lib.get(url)
            return response.content
        except requests.RequestException as exc:
            raise JournalException(exc)

    def get_index_page(self, page_nr):
        """
        Gets an index page for a specific `page_nr`

        :param page_nr: Page number to get the content for
        :type page_nr: int

        :returns: Content of the page
        :rtype: str
        """
        query_params = {'p': str(page_nr)}
        encoded_query_params = urlencode(query_params, doseq=True)
        page_url = ParseResult(
            scheme=self.parsed_base_url.scheme,
            netloc=self.parsed_base_url.netloc,
            path=self.parsed_base_url.path,
            params=self.parsed_base_url.params,
            query=encoded_query_params,
            fragment=self.parsed_base_url.fragment).geturl()
        LOG.debug(
            "Get content for page_nr %s from url %s", page_nr, page_url)
        return self.get(page_url)
