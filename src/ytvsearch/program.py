"""
Program class.

Attributes:
    date: ex. '2020/01/11'
    time: ex. 'foobar'
    is_on_air: true if the tv program is now on air.
    title: program title
    is_repeated: true if the tv program is repeated.
    channel: tv channel name
    genre: {
        'parent': parent genre ex. '趣味／教育'
        'child':  child genre ex. '生涯教育・資格'
    }
    description: description of tv program
    impression_num: a number of impressions
    evaluation: {
        'average_pts': average evaluation point (max = 5)
        'total_num_vote': a number of vote count
    }
    mitai_num: a number of '見たい!' count
"""


class Program:
    def __init__(self):
        self.date = {
            'start': None,
            'end': None,
        }
        self.is_on_air = False

        self.title = ''
        self.is_repeated = False
        self.channel = ''

        self.genre = {
            'parent': '',
            'child': '',
        }
        self.description = ''

        self.impression_num = 0
        self.evaluation = {
            'average_pts': 0,
            'total_num_vote': 0,
        }
        self.mitai_num = 0
