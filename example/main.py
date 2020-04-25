# Search module
from ytvsearch.searcher import Searcher
# Search options
from ytvsearch.search_option import SearchOption


# Search keyword
KEYWORD = '北海道'

if __name__ == '__main__':
    # Create instance
    tv_searcher = Searcher()
    # Run search
    tv_programs = tv_searcher.run(
        keyword=KEYWORD,
        # Broad types. Terrestrial (地上波) and BS
        broad_types=[
            SearchOption.Broadcast.TERRESTRIAL,
            SearchOption.Broadcast.BS,
        ],
        # Limit
        fetch_limit=20
    )

    # Obtained programs is type of list.
    for tv_program in tv_programs:
        print('{date}: {title} ({channel})'.format(
            date=tv_program.date['start'],
            title=tv_program.title,
            channel=tv_program.channel
        ))
