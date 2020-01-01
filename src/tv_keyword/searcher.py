import time
import requests
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from src.tv_keyword.program import Program


URL_BASE = 'https://tv.yahoo.co.jp/search/?q='
SLEEP_SEC = 3


class Searcher:
    def __init__(self, *, keyword: str, url_base=URL_BASE):
        self.keyword = keyword
        self.url_base = url_base

        parsed_url = urlparse(url_base)
        self.url_scheme = parsed_url.scheme
        self.url_domain = parsed_url.netloc

    def run(self, *, url='') -> list:
        programs = []
        if not url:
            url = '{}/{}'.format(self.url_base, self.keyword)

        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'html.parser')

        for prog in soup.select('.programlist > li'):
            program = Program()

            date_element = prog.select_one('.leftarea')
            program.date = date_element.select_one('.yjMS > em').get_text()
            program.time = date_element.select_one('.yjMS ~ p > em').get_text()
            program.is_on_air = date_element.select_one(
                '.mt10 > .onAir.yjMS'
            ) is not None

            p_details = prog.select_one('.rightarea')
            program.title = p_details.select_one('.yjLS.pb5p').get_text()

            sub_texts = p_details.select('.yjMS.pb5p')
            program.channel = sub_texts[0].select_one('.pr35').get_text()

            genre_element = sub_texts[0].select('.pr35 ~ span > a')
            program.genre = {
                'child': genre_element[0].get_text(),
                'parent': genre_element[1].get_text(),
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

            programs.append(program)

        next_url = self._get_next_url(soup)
        if next_url:
            time.sleep(SLEEP_SEC)
            programs.extend(self.run(url=next_url))

        return programs

    def _get_next_url(self, soup):
        navi_element = soup.select('div.yjMS.search_number.mb10 > p.floatr > a')
        if len(navi_element) < 2:
            return None

        path = navi_element[1].get('href')
        if not path:
            return None

        return '{0}://{1}{2}'.format(self.url_scheme, self.url_domain, path)
