import pandas as pd
import numpy as np
# from libs import common


def check_for_optimized_df_data_types(df : pd.DataFrame):
    current_dtype = None
    optimized_dtype = None
    for i, col in enumerate(df.columns,1):
        current_dtype = df[col].dtype
        if pd.api.types.is_integer_dtype(df[col]) or pd.api.types.is_float_dtype(df[col]):
            max_val : int = max(df[col])
            if pd.api.types.is_integer_dtype(df[col]):
                if max_val < 256:
                    optimized_dtype = np.uint8
                elif 255 < max_val < 65535:
                    optimized_dtype = np.uint16
                elif 65535 < max_val < 4294967295:
                    optimized_dtype = np.uint32
                else:
                    max_val = None
                    optimized_dtype = "too high"
            elif pd.api.types.is_float_dtype(df[col]):
                df1 = df[df[col].isna() == False]
                print(col)
                if all([r for r in df[df[col].isna() == False].itertuples() if r[i] == int(r[i])]):
                    print(f'{col}  Can be int')
                else:
                    print(f'{col}  Can\'t ne int')
                break
                # any([r for r in df[df['strikeRate'].isna() == False].itertuples() if r.strikeRate != int(r.strikeRate)])
                max_val : int = max(df[col])
                if max_val < 256:
                    optimized_dtype = np.uint8
                elif 255 < max_val < 65535:
                    optimized_dtype = np.uint16
                elif 65535 < max_val < 4294967295:
                    optimized_dtype = np.uint32
                else:
                    max_val = None
                    optimized_dtype = "too high"
        else:
            max_val = None
            optimized_dtype = "Column datatype NOT numeric"
        # if max_val != None:
        #     print(f'Column: {col}; Max Value: {max_val}; Current data type: {current_dtype}; Possile optimized Data type: {optimized_dtype}')
    
