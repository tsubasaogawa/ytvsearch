import pathlib
import sys

current_dir = pathlib.Path(__file__).resolve().parent
sys.path.append(str(current_dir) + '/../')

from src.tv_keyword.program import Program
from src.tv_keyword.searcher import Searcher


KEYWORD = '北海道'

if __name__ == '__main__':
    searcher = Searcher(keyword=KEYWORD)
    programs = searcher.run()

    for program in programs:
        print(program.title)
