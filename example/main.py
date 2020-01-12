from ytvsearch.searcher import Searcher
from ytvsearch.search_option import SearchOption


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
        print('{date}: {title} ({channel})'.format(
            date=tv_program.date['start'],
            title=tv_program.title,
            channel=tv_program.channel
        ))
