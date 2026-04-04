import pandas as pd
import query

# gets top 500 most reviewed games on steam
player_ct = query.query_to_df('popularity_primitives', 'fields game_id, popularity_type, value;'
                              'where popularity_type = 8;'
                              'sort value desc;'
                              'limit 500;'
                              'offset 0;')
# build id_list lookup helper
id_list = query.df_to_feature(player_ct, "game_id")
#match id -> name
name_df = query.query_to_df(
    'games',
    f'fields id, name; where id = ({id_list}); limit 500;'
)

merged_df = player_ct.merge(
    name_df,
    left_on="game_id",
    right_on="id"
)

merged_df = merged_df.sort_values("value", ascending=False)

print(merged_df[["name", "value"]].to_string())