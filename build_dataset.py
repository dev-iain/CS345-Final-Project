import pandas as pd
from query import query_to_df

print("Building dataset...")

all_dfs = []

for offset in range(0, 2000, 500):
    print(f"Fetching offset {offset}")
    
    df = query_to_df(
        "games",
        """
        fields id, name,
               aggregated_rating, aggregated_rating_count,
               follows, hypes,
               genres, platforms,
               first_release_date;
        where platforms = [6] & aggregated_rating != null;
        """,
        limit = 500,
        offset = offset
    )
    
    if df.empty:
        print("Completed")
        break
    
    all_dfs.append(df)
    
games_df = pd.concat(all_dfs, ignore_index = True)

print(f"Total rows collected: {len(games_df)}")

games_df.to_csv("games_raw.csv", index = False)

print("Saved to games_raw.csv")