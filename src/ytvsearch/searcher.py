"""
Searcher class

Searcher returns keyword-related tv programs from yahoo japan.
"""

import logging
import time
import requests

from urllib.parse import urlparse
from bs4 import BeautifulSoup

from .program import Program
from .search_option import SearchOption
from ytvsearch import ydatetime


# Define default values
DEFAULTS = {
    'url_base': 'https://tv.yahoo.co.jp/search/',
    'sleep_sec': 1,
    'show_num_in_page': 10,
}


class Searcher:
    def __init__(self, *,
                 url_base: str = DEFAULTS['url_base']):
        """
        Constructor.

        Args:
            url_base (optional): yahoo tv search url without query parameters
        """
        self._url_base = url_base

        parsed_url = urlparse(url_base)
        self._url_scheme = parsed_url.scheme
        self._url_domain = parsed_url.netloc

        # paging index in scraping
        self._page_index = 0
        # scraping url as pointer
        self._url = ''

    def run(self, *,
            keyword: str = '',
            broad_types: list = [SearchOption.Broadcast.TERRESTRIAL],
            prefecture: SearchOption.Prefecture = SearchOption.Prefecture.TOKYO,
            oa: int = 1,
            fetch_limit: int = 0) -> list:
        """
        Run scraping.

        Args:
            keyword: keyword for search
            broad_types (optional): search option; see SearchOption.Broadcast
            prefecture (optional): search option; see SearchOption.Prefecture
            oa (optional): search option; constant value
            fetch_limit (optional): limit number of tv program to fetch

        Returns:
            list: program list; see Program class
        """
        # First run
        if not self._url:
            if not keyword:
                raise RuntimeError('either url or keyword is not empty')
            # set search url with given arguments
            self._url = self._generate_start_url(
                keyword,
                broad_types=broad_types,
                prefecture=prefecture,
                oa=oa
            )
            self._page_index = 0

        res = requests.get(self._url)
        soup = BeautifulSoup(res.text, 'html.parser')

        programs = []
        # base count of total number of programs
        total_base = self._page_index * DEFAULTS['show_num_in_page']
        for i, prog_elem in enumerate(soup.select('.programlist > li')):
            total = total_base + i
            # reach limit count
            if fetch_limit > 0 and total >= fetch_limit:
                self._url = ''
                return programs

            programs.append(self._convert_to_program_object(prog_elem))

        # set next url from scraped html
        self._url = self._get_next_url(soup)
        logging.debug('next_url is {0}'.format(self._url))
        if self._url:
            time.sleep(DEFAULTS['sleep_sec'])
            self._page_index += 1
            programs.extend(self.run(fetch_limit=fetch_limit))

        return programs

    def _convert_to_program_object(self, prog_element) -> Program:
        """
        Convert program element to program object.

        Args:
            prog_element: program element by beautifulsoup

        Returns:
            Program: program object
        """
        program = Program()

        date_element = prog_element.select_one('.leftarea')
        program.date['start'], program.date['end'] = ydatetime.convert_to_datetimes(
            date_element.select_one('.yjMS > em').get_text(),
            date_element.select_one('.yjMS ~ p > em').get_text()
        )
        program.is_on_air = date_element.select_one(
            '.mt10 > .onAir.yjMS'
        ) is not None

        detail_element = prog_element.select_one('.rightarea')
        title_element = detail_element.select_one('.yjLS.pb5p')
        program.title = title_element.select_one('.yjLS.pb5p > a').get_text()
        program.is_repeated = title_element.select_one(
            '.icon_repeat') is not None
        sub_texts = detail_element.select('.yjMS.pb5p')
        program.channel = sub_texts[0].select_one('.pr35').get_text()
        genre_element = sub_texts[0].select('.pr35 ~ span > a')
        program.genre = {
            'child': genre_element[0].get_text(),
            'parent': genre_element[1].get_text(),
        } if genre_element else {
            'child': '',
            'parent': '',
        }
        program.description = sub_texts[1].get_text()
        program.impression_num = int(
            sub_texts[2].select_one('.pr35.floatl > a').get_text()
        )
        evaluation_element = sub_texts[2].select('.pr20 > em')
        program.evaluation = {
            'average_pts': float(evaluation_element[0].get_text()),
            'total_num_vote': 0 if len(evaluation_element) == 1 else int(
                evaluation_element[1].get_text()
            ),
        }
        program.mitai_num = int(
            sub_texts[2].select_one('.mitaiTxt').get_text()
        )

        return program

    def _get_next_url(self, soup) -> str:
        """
        Get next url from scraped html.

        Args:
            soup: beautifulsoup object

        Returns:
            str: url; empty if url is not found
        """
        navi_element = soup.select(
            'div.yjMS.search_number.mb10 > p.floatr > a')
        if len(navi_element) < 2:
            return ''

        path = navi_element[1].get('href')
        if not path:
            return ''

        return '{0}://{1}{2}'.format(self._url_scheme, self._url_domain, path)

    def _generate_start_url(self,
                            keyword: str,
                            *,
                            broad_types: list,
                            prefecture: SearchOption.Prefecture,
                            oa: int,
                            start_num: int = 1) -> str:
        """
        Generate url with search keyword and some options.

        Args:
            keyword: search keyword
            broad_types: search option; see SearchOption.Broadcast
            prefecture: search option; see SearchOption.Prefecture
            oa: search option; constant value
            start_num: start number of search items

        Returns:
            string: url
        """
        if type(broad_types) is not list:
            raise TypeError('type of broad_types is list')

        for broad_type in broad_types:
            if type(broad_type) is not SearchOption.Broadcast:
                raise TypeError('type of broad_type is SearchOption.Broadcast')

        broad_types_query = ' '.join(sorted(map(str, broad_types)))

        if type(prefecture) is not SearchOption.Prefecture:
            raise TypeError('type of prefecture is SearchOption.Prefecture')

        return '{base}?q={kwd}&t={broad}&a={pref}&oa={oa}&s={start}'.format(
            base=self._url_base,
            kwd=keyword,
            broad=broad_types_query,
            pref=prefecture,
            oa=oa,
            start=start_num
        )
