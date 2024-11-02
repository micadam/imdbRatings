#!/usr/bin/env python
import os
from pathlib import Path

import pandas as pd

INDEX_COL = "tconst"
TITLE_TYPE_COL = "titleType"
PRIMARY_TITLE_COL = "primaryTitle"
NUM_VOTES_COL = "numVotes"
PARENT_TCONST_COL = "parentTconst"
SEASON_NUMBER_COL = "seasonNumber"
EPISODE_NUMBER_COL = "episodeNumber"
AVERAGE_RATING_COL = 'averageRating'

SCRIPT_DIR = Path(os.path.dirname(os.path.realpath(__file__)))

print("Loading data")
basics = pd.read_table(SCRIPT_DIR / "data/basics.tsv", index_col=INDEX_COL)
tv_episodes = pd.read_table(SCRIPT_DIR / "data/episode.tsv",
                            index_col=INDEX_COL,
                            dtype={EPISODE_NUMBER_COL: pd.Int64Dtype(), SEASON_NUMBER_COL: pd.Int64Dtype()},
                            na_values="\\N")
ratings = pd.read_table(SCRIPT_DIR / "data/ratings.tsv", index_col=INDEX_COL)

basics = basics.join(ratings)

series = basics[basics[TITLE_TYPE_COL] == "tvSeries"]
episodes = basics[basics[TITLE_TYPE_COL] == "tvEpisode"]

episodes = episodes.join(tv_episodes)
print("Data loaded")


def fetch(title: str) -> pd.DataFrame:
    my_id = series[series[PRIMARY_TITLE_COL].str.lower() == title.lower()].sort_values(NUM_VOTES_COL, ascending=False).index[0]
    my_episodes = episodes[episodes[PARENT_TCONST_COL] == my_id]
    return my_episodes.sort_values([SEASON_NUMBER_COL, EPISODE_NUMBER_COL])
