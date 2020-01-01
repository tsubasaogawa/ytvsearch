import requests
from bs4 import BeautifulSoup
from src.tv_keyword.program import Program


URL_BASE = 'https://tv.yahoo.co.jp/search/?q='


class Searcher:
    def __init__(self, *, url_base=URL_BASE):
        self.url_base = url_base

    def run(self, *, keyword: str) -> list:
        programs = []
        res = requests.get('{}/{}'.format(self.url_base, keyword))
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

        return programs
