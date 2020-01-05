import pathlib
import sys

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + '/../')

from src.tv_keyword.searcher import Searcher
from src.tv_keyword.search_option import SearchOption


KEYWORD = '北海道'

if __name__ == '__main__':
    tv_searcher = Searcher()
    tv_programs = tv_searcher.run(
        keyword=KEYWORD,
        broad_types=[
            SearchOption.Broadcast.TERRESTRIAL,
            SearchOption.Broadcast.BS,
        ],
        fetch_limit=20
    )

    for tv_program in tv_programs:
        print('{date} {time}: {title} ({channel})'.format(
            date=tv_program.date,
            time=tv_program.time,
            title=tv_program.title,
            channel=tv_program.channel
        ))
