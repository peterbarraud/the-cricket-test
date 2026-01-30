from pandas import DataFrame
from pandas.api.types import is_numeric_dtype
from numpy import iinfo,uint8,uint16,uint32

def optimize_df(df : DataFrame, do_optimize = False,displayOutput=True):
    memory_usage = df.memory_usage(deep=True).sum()
    for col in df.columns:
        if is_numeric_dtype(df[col]):
            if max(df[col]) < iinfo(uint8).max:
                if do_optimize:
                    df[col] = df[col].astype(uint8)
                    if displayOutput:
                        print(f"{col} is optimized to: {uint8}")
                else:
                    print(f"{col} can be optimized to: {uint8}")
            else:
                if iinfo(uint8).max < max(df[col]) < iinfo(uint16).max:
                    if do_optimize:
                        df[col] = df[col].astype(uint16)
                        if displayOutput:
                            print(f"{col} is optimized to: {uint16}")
                    else:
                        print(f"{col} can be optimized to: {uint16}")
                else:
                    if iinfo(uint16).max < max(df[col]) < iinfo(uint32).max:
                        if do_optimize:
                            if displayOutput:
                                print(f"{col} is optimized to: {uint32}")
                            df[col] = df[col].astype(uint32)
                        else:
                            print(f"{col} can be optimized to: {uint16}")
                    else:
                        if displayOutput:
                            print(f"{col} cannot be optimized further")
    memory_reduction = df.memory_usage(deep=True).sum()-memory_usage
    improvement = round((memory_reduction/memory_usage)/100,2)
    print(f"Memory improved by: {(improvement)}")