from libs.csvnames import CSVName
from libs.optimizer import optimize_df
from pandas import read_csv, DataFrame

def get_dataframe_by_name(csvName : CSVName, optimizeDf : bool = True,  usecols=list(),showOutput=True) -> DataFrame:
    df : DataFrame = None
    if len(usecols):
        df : DataFrame = read_csv(f'data/{csvName.name.lower()}.csv',usecols=usecols)
    else:
        df : DataFrame = read_csv(f'data/{csvName.name.lower()}.csv')
    if optimizeDf:
        optimize_df(df,do_optimize=True,displayOutput=showOutput)
    return df


