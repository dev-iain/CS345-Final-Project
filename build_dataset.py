import pandas as pd
from query import query_to_df, df_to_feature
from pathlib import Path
import os

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

def delete(filepath):
    if os.path.exists(filepath):
        os.remove(filepath)
    else:
        print("File does not exist.")

def clear(dir_path):
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted file: {filename}")

def updateAll(limit=100):
    clear("datasets")
    buildAll(limit)

def buildAll(limit):
    most_reviewed_df = build(limit, 
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
    
    pos_popscore = build(
        limit, 
        "popularity_primitives",
        f"""
        fields game_id, value;
        where game_id = ({review_lookup}) & popularity_type = 6;
        """,
        500,
        0
    )
    pos_popscore = pos_popscore.rename(columns = {"value": "positive_reviews"})

    neg_popscore = build(
        limit,
        "popularity_primitives",
        f"""
        fields game_id, value;
        where game_id = ({review_lookup}) & popularity_type = 7;
        """,
        500,
        0
    )
    neg_popscore = neg_popscore.rename(columns={"value": "negative_reviews"})

    games_raw_df = build(
            limit,             
           "games",
            f"""
            fields id,
                aggregated_rating, aggregated_rating_count, 
                rating, rating_count,
                follows, first_release_date;
            where id = ({review_lookup}) & platforms = [6] & aggregated_rating != null;
            """,
            500, 
            0
           )
    games_raw_df = games_raw_df.set_index("id")
    games_raw_df = games_raw_df.join(pos_popscore.set_index("game_id")[["positive_reviews"]])
    games_raw_df = games_raw_df.join(neg_popscore.set_index("game_id")[["negative_reviews"]])
    print(games_raw_df.to_string())
    save(games_raw_df, "datasets/games_raw")

updateAll(500)

