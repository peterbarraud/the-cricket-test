from libs.csvnames import CSVName
from libs.optimizer import optimize_df
from pandas import read_csv, DataFrame
from datetime import datetime,timedelta

def get_dataframe_by_name(csvName : CSVName, optimizeDf : bool = True,  usecols=list(),showOutput=True) -> DataFrame:
    df : DataFrame = None
    csv_path : str = f'data/{csvName.name.lower()}.csv'
    if len(usecols):
        df : DataFrame = read_csv(csv_path,usecols=usecols)
    else:
        df : DataFrame = read_csv(csv_path)
    if optimizeDf:
        optimize_df(df,do_optimize=True,displayOutput=showOutput)
    return df

def get_datetime_from_epoch(df: datetime,epoch:int):
    dt : datetime = None
    if epoch < 0:
        dt = datetime(1970, 1, 1) + timedelta(seconds=epoch)
    else:
        dt = datetime.fromtimestamp(epoch)
    return dt



