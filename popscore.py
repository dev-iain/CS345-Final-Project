import pandas as pd
import query
import numpy as np
# gets top 500 most reviewed games on steam
LIMIT = 500
player_rvw = query.query_to_df('popularity_primitives', 'fields game_id, value;'
                              'where popularity_type = 8;'
                              'sort value desc;',
                              LIMIT, 0)
player_rvw = player_rvw.rename(columns={"value": "review_count"})

# build id_list lookup helper
id_list = query.df_to_feature(player_rvw, "game_id")

#build rest of data
pos_rvw = query.query_to_df('popularity_primitives', 'fields game_id, value;'
                            f'where game_id = ({id_list}) & popularity_type = 6;',
                            LIMIT, 0)
pos_rvw = pos_rvw.rename(columns = {"value": "positive_reviews"})

neg_rvw = query.query_to_df('popularity_primitives', 'fields game_id, value;'
                            f'where game_id = ({id_list}) & popularity_type = 7;',
                            LIMIT, 0)
neg_rvw = neg_rvw.rename(columns={"value": "negative_reviews"})

#match id -> name
name_df = query.query_to_df(
    'games',
    f'fields id, name; where id = ({id_list});', LIMIT, 0
)

game_df = name_df.set_index("id").join(player_rvw.set_index("game_id")[["review_count"]])
game_df = game_df.join(pos_rvw.set_index("game_id")[["positive_reviews"]])
game_df = game_df.join(neg_rvw.set_index("game_id")[["negative_reviews"]])
game_df["normalized"] = (game_df["positive_reviews"] - game_df["negative_reviews"]) / np.log1p(game_df["review_count"])
print(game_df.sort_values(by="normalized", ascending=False))

