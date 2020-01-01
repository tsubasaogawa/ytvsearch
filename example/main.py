import pathlib
import sys
current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + '/../')

from src.tv_keyword.searcher import Searcher


KEYWORD = '北海道'

if __name__ == '__main__':
    searcher = Searcher()
    programs = searcher.run(keyword=KEYWORD)

    print(programs)
