from libs.csvnames import CSVName
from libs.optimizer import optimize_df
from pandas import read_csv, DataFrame

def get_dataframe_by_name(csvName : CSVName, optimizeDf : bool = True,  usecols=list()) -> DataFrame:
    df : DataFrame = read_csv(f'data/{csvName.name.lower()}.csv',usecols=usecols)
    if optimizeDf:
        optimize_df(df,do_optimize=True)
    return df


