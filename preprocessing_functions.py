import numpy as np 
import pandas as pd

def create_unit_indicator(df):
    # Create an indicator of First, Second and Third Unit by minutes played
    df["MP_Rank"] = df.groupby(["Season", "Team"])["MP"].rank("dense", ascending = False)

    conditions = [

        # First Unit
        (df["MP_Rank"] >= 1) & (df["MP_Rank"] < 6),
        # Second Unit
        (6 <= df["MP_Rank"]) & (df["MP_Rank"] < 11),
        # Third Unit
        (11 <= df["MP_Rank"]),
    ]

    unit = [1,2,3]

    # Create a column when meet conditions criteria
    df["Unit"] = np.select(conditions, unit)

    return df

def sum_stat_by_unit(player_stats, unit, stat):
    return player_stats[player_stats.Unit == unit].groupby(["Team", "Season"]).sum()[stat]
