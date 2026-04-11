import pandas as pd
from query import query_to_df



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


save(build(
            2000,             
           "games",
            """
            fields id, name,
                aggregated_rating, aggregated_rating_count,
                follows, hypes,
                genres, platforms,
                first_release_date;
            where platforms = [6] & aggregated_rating != null;
            """,
            500, 
            0
           ), 
     "datasets/games_raw", index=False)
