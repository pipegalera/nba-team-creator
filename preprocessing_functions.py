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

def create_summed_PER_by_units(df):
    # Calculate the summed PER of the different units 
    per = df[["Player", "Team", "Season", "Unit", "PER"]]
    per = pd.pivot_table(data = per, values = "PER", index = ["Team", "Season", "Unit"], aggfunc= np.sum).reset_index()

    # PER summed of all units
    per_123_units = per.groupby(["Team", "Season"]).sum()["PER"].reset_index()
    per_123_units["PER_Rank_all"] = per_123_units.groupby("Season")["PER"].rank("dense", ascending = False)
    per_123_units.rename({"PER": "PER_Sum_all"}, axis = 1, inplace = True)

    # PER summed of first and second unit
    per = per[per.Unit != 3]
    per_12_units = per.groupby(["Team", "Season"]).sum()["PER"].reset_index()
    per_12_units["PER_Rank_FU_SU"] = per_12_units.groupby("Season")["PER"].rank("dense", ascending = False)
    per_12_units.rename({"PER": "PER_Sum_FU_SU"}, axis = 1, inplace = True)

    # PER summed of first unit
    per = per[per.Unit != 2]
    per_1_units = per.groupby(["Team", "Season"]).sum()["PER"].reset_index()
    per_1_units["PER_Rank_FU"] = per_1_units.groupby("Season")["PER"].rank("dense", ascending = False)
    per_1_units.rename({"PER": "PER_Sum_FU"}, axis = 1, inplace = True)

    # Merge all dataframes 

    PER_Rank = per_1_units.merge(per_12_units).merge(per_123_units)
    
    return PER_Rank