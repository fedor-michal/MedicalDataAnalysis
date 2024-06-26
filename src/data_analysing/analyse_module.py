import pandas as pd

def get_no_show_percentage(column: str, value, dataframe: pd.DataFrame) -> float:
    no_show_count = len(dataframe[(dataframe[column] == value) & (dataframe["No-show"] == "Yes")])
    all_count = len(dataframe[(dataframe[column] == value)])
    perc_no_show = (no_show_count / all_count) * 100
    return perc_no_show

def get_counts(dataframe: pd.DataFrame, column: str, value) -> int:
    count = len(dataframe[(dataframe[column]) == value])
    return count

def get_counts_with_parameter(dataframe: pd.DataFrame, column: str, value, column_2: str, value_2) -> int:
    count = len(dataframe[(dataframe[column] == value) & (dataframe[column_2] == value_2)])
    return count

def get_counts_between_values_with_parameter(dataframe: pd.DataFrame, column: str, value_1, value_2,
                                             parameter_column: str, parameter_value) -> int:
    count = len(dataframe[(dataframe[column] >= value_1) & (dataframe[column] <= value_2)
                          & (dataframe[parameter_column] == parameter_value)])
    return count