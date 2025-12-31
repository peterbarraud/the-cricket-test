import pandas as pd
import numpy as np

def change_type(df, field_name, d_type):
    max_before = max(df[field_name])
    df[field_name] = df[field_name].astype(d_type)
    if max_before != max(df[field_name]):
        raise Exception(f"Something happended in change type for: {field_name}")

def get_datatype_info(csvFile : str):
    intrange : dict = {'uint8':255,'uint16':65535,'uint32':4294967295}
    df : pd.DataFrame = pd.read_csv(csvFile)
    f = open('logs/test_Matches_Data.csv','w')
    f.write('Name,Data type,Max value,Optimized data type\n')
    for col in df.columns:
        max_value = max(df[col]) if str(df[col].dtype).startswith('int') or str(df[col].dtype).startswith('float') else ''
        optimized_data_type = None
        if str(df[col].dtype).startswith('int') or str(df[col].dtype).startswith('float'):
            if max_value < intrange['uint8']:
                optimized_data_type = np.uint8
            elif intrange['uint8'] <= max_value < intrange['uint16']:
                optimized_data_type = np.uint16
            elif intrange['uint16'] <= max_value < intrange['uint32']:
                optimized_data_type = np.uint
            else:
                optimized_data_type = intrange['uint64']
            try:
                change_type(df, col,optimized_data_type)
            except Exception as ex:
                print(col)
                print(ex)
                print("*"*100)
        f.write(f'{col},{df[col].dtype},{max_value}\n')

    # for row in df.info().iterrows():
    #     print(row)
    df_file = csvFile.replace('.csv','df')
    df.to_pickle(df_file)
    print("all good")
    f.close()

def create_dt_optimized_df(csvFile : str):
    df : pd.DataFrame = pd.read_csv(csvFile)


    df.to_pickle(csvFile.replace('.csv','.df'))

def main():
    create_dt_optimized_df('data/test_Matches_Data.csv')
    # get_datatype_info('data/test_Matches_Data.csv')

if __name__ == "__main__":
    main()