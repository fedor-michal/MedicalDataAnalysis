import pandas as pd

def get_no_show_percentage(column: str, value, dataframe: pd.DataFrame) -> float:
    no_show_count = len(dataframe[(dataframe[column] == value) & (dataframe["No-show"] == "Yes")])
    all_count = len(dataframe[(dataframe[column] == value)])
    perc_no_show = (no_show_count / all_count) * 100
    return perc_no_show

def get_counts(dataframe: pd.DataFrame, column: str, value) -> int:
    count = len(dataframe[(dataframe[column]) == value])
    return count