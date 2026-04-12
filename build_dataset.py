import pandas as pd
from query import query_to_df, df_to_feature



def build(max, endpoint, query, limit, offset):
    print("Building dataset...")
    all_dfs = []
    
    for offset in range(0, max, limit):
        print(f"Fetching offset {offset}")
        
        df = query_to_df(
            endpoint,
            query,
            limit,
            offset
        )
        if df.empty:
            print("Completed")
            break
        all_dfs.append(df)
        
    games_df = pd.concat(all_dfs, ignore_index = True)
    
    print(f"Total rows collected: {len(games_df)}")
    
    return games_df
    
def save(df, filename, **kwargs):
    df.to_csv(f'{filename}.csv', **kwargs)
    print(f"Saved to {filename}.csv")


most_reviewed_df = build(5000, 
                         'popularity_primitives', 
                         """
                        fields game_id, value;
                        where popularity_type = 8;
                        sort value desc;
                         """,
                        500,
                        0
                    )

save(most_reviewed_df, "datasets/most_reviewed", index=False)
review_lookup = df_to_feature(most_reviewed_df, "game_id")

save(build(
            5000,             
           "games",
            f"""
            fields id, name,
                aggregated_rating, aggregated_rating_count,
                follows, hypes,
                genres, platforms,
                first_release_date;
            where id = ({review_lookup}) & platforms = [6] & aggregated_rating != null;
            """,
            500, 
            0
           ), 
     "datasets/games_raw", index=False)
                        