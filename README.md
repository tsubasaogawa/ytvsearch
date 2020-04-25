# ytvsearch

[![CircleCI](https://circleci.com/gh/tsubasaogawa/ytvsearch.svg?style=svg)](https://circleci.com/gh/tsubasaogawa/ytvsearch)

## Overview

- A simple tv program api by scraping [Yahoo Japan 番組表](https://tv.yahoo.co.jp/listings/realtime/).
- Search tv programs using
  - keyword
  - broad types (ex. BS, CS, terrestrial)
  - prefecture

## Install

```bash
pip install ytvsearch
```

## Sample

### Source code

See `example` directory.

```python
from ytvsearch.searcher import Searcher
from ytvsearch.search_option import SearchOption


tv_searcher = Searcher()
tv_programs = tv_searcher.run(
    keyword='北海道',
    broad_types=[ SearchOption.Broadcast.TERRESTRIAL ],
    fetch_limit=10
)

for tv_program in tv_programs:
    print('{date}: {title} ({channel})'.format(
        date=tv_program.date['start'],
        title=tv_program.title,
        channel=tv_program.channel
    ))
```

### Output

```text
2020-04-25 21:00:00+09:00: NHKスペシャル▽新型コロナウイルス　どうなる緊急事態宣言～医療と経済の行方～ (NHK総合1・東京（地上波）)
2020-04-26 04:30:00+09:00: イッピン・選「個性が光る　北の大地の器～北海道　札幌の焼き物～」 (NHK総合1・東京（地上波）)
2020-04-26 07:45:00+09:00: さわやか自然百景「早春　北海道　石狩湾」 (NHK総合1・東京（地上波）)
2020-04-26 13:35:00+09:00: ニッポンの里山　ふるさとの絶景に出会う旅「シマエナガ舞う北国の森　北海道占冠村」 (NHK総合1・東京（地上波）)
2020-04-27 11:00:00+09:00: 韓国ドラマ「ラブレイン」　★第19話「ねじれた運命」 (TOKYO　MX1（地上波）)
2020-04-28 01:28:00+09:00: 週刊EXILE　まだまだあった三代目JSB10か月長期密着未公開SP!裏話も! (TBS1（地上波）)
2020-04-28 11:00:00+09:00: 韓国ドラマ「ラブレイン」　★第20話「愛の誓い」 (TOKYO　MX1（地上波）)
2020-04-29 09:00:00+09:00: 小さな旅　選「特集　山の歌　総集編」 (NHK総合1・東京（地上波）)
2020-04-30 00:15:00+09:00: NHKスペシャル▽新型コロナウイルス　どうなる緊急事態宣言～医療と経済の行方 (NHK総合1・東京（地上波）)
2020-04-30 02:35:00+09:00: 日本夜景めぐり「北海道」 (NHK総合1・東京（地上波）)
```

## License

MIT
