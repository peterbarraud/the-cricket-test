from pandas import DataFrame
from pandas.api.types import is_numeric_dtype
from numpy import iinfo,uint8,uint16,uint32,int8,int16,int32

def optimize_df(df : DataFrame, do_optimize = False,displayOutput=True):
    memory_usage = df.memory_usage(deep=True).sum()
    for col in df.columns:
        if is_numeric_dtype(df[col]):
            astype = None
            if min(df[col]) < 0:
                if max(df[col]) <= iinfo(int8).max:
                    astype = int8
                elif max(df[col]) <= iinfo(int16).max:
                    astype = int16
                elif max(df[col]) <= iinfo(int32).max:
                    astype = int32
            else:
                if max(df[col]) <= iinfo(uint8).max:
                    astype = uint8
                elif max(df[col]) <= iinfo(uint16).max:
                    astype = uint16
                elif max(df[col]) <= iinfo(uint32).max:
                    astype = uint32
            if astype is not None:
                if do_optimize:
                    df[col] = df[col].astype(astype)
                    if displayOutput:
                        print(f"{col} is optimized to {astype}")
                else:
                    print(f"{col} can be optimized to {astype}")
            else:
                if displayOutput:
                    print(f"{col} cannot be optimized further")
    memory_reduction = memory_usage-df.memory_usage(deep=True).sum()
    improvement = round((memory_reduction/memory_usage)*100,2)
    print(f"Memory improved by: {(improvement)}%")