import logging
import time
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from .program import Program
from .search_option import SearchOption


URL_BASE = 'https://tv.yahoo.co.jp/search/'
SLEEP_SEC = 1
SHOW_NUM_IN_PAGE = 10


class Searcher:
    def __init__(self, *,
                 url_base: str = URL_BASE
                 ):
        self.url_base = url_base

        parsed_url = urlparse(url_base)
        self.url_scheme = parsed_url.scheme
        self.url_domain = parsed_url.netloc

        self.page_index = 0
        self.url = ''

        # logging.basicConfig(level=logging.DEBUG)

    def run(self, *,
            keyword: str = '',
            broad_types: list = [SearchOption.Broadcast.TERRESTRIAL],
            prefecture: int = SearchOption.Prefecture.TOKYO,
            oa: int = 1,
            fetch_limit: int = 0
            ) -> list:
        # First run
        if not self.url:
            if not keyword:
                raise RuntimeError('either url or keyword is not null')
            self.url = self._generate_start_url(
                keyword,
                broad_types=broad_types,
                prefecture=prefecture,
                oa=oa
            )
            self.page_index = 1

        res = requests.get(self.url)

        soup = BeautifulSoup(res.text, 'html.parser')

        programs = []
        total_base = self.page_index * SHOW_NUM_IN_PAGE
        for i, prog in enumerate(soup.select('.programlist > li')):
            if fetch_limit > 0 and total_base + i >= fetch_limit:
                self.url = ''
                return programs

            programs.append(self._fetch_program_data(prog))

        self.url = self._fetch_next_url(soup)
        logging.debug('next_url is {0}'.format(self.url))
        if self.url:
            time.sleep(SLEEP_SEC)
            self.page_index += 1
            programs.extend(self.run(fetch_limit=fetch_limit))

        return programs

    def _fetch_program_data(self, prog_element) -> Program:
        program = Program()

        date_element = prog_element.select_one('.leftarea')
        program.date = date_element.select_one('.yjMS > em').get_text()
        program.time = date_element.select_one('.yjMS ~ p > em').get_text()
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

    def _fetch_next_url(self, soup) -> str:
        navi_element = soup.select(
            'div.yjMS.search_number.mb10 > p.floatr > a')
        if len(navi_element) < 2:
            return ''

        path = navi_element[1].get('href')
        if not path:
            return ''

        return '{0}://{1}{2}'.format(self.url_scheme, self.url_domain, path)

    def _generate_start_url(self,
                            keyword: str,
                            *,
                            broad_types: list,
                            prefecture: SearchOption.Prefecture,
                            oa: int,
                            start_num: int = 1
                            ) -> str:
        broad_types_query = ' '.join(sorted(map(str, broad_types)))

        return '{base}?q={kwd}&t={broad}&a={pref}&oa={oa}&s={start}'.format(
            base=URL_BASE,
            kwd=keyword,
            broad=broad_types_query,
            pref=prefecture,
            oa=1,
            start=start_num
        )
