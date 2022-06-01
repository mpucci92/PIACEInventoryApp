import pandas as pd
import numpy as np
import os
import glob as glob
import datetime

date = datetime.datetime.now()

dir_path = os.path.dirname(os.path.realpath(__file__))

def largestChain(df, col):
    listLength = []

    for element in df[col].apply(lambda x: x.split("\\")):
        listLength.append(len(element))

    return max(listLength)

def renameCols(df):
    renamed_columns = ['Module','AceScheduler_AceLibraries']
    for i in range(len(df.columns)):
        if i == 0 or i == 1:
            continue
        renamed_columns.append(f'AceComponent_{i-1}')
    return renamed_columns


def columnStats(df):
    anchor = 'AceScheduler_AceLibraries'
    calculated = list(df.columns[2:].values)

    for col in calculated:
        (final_df.groupby(by=[anchor, col]).size().unstack(fill_value=0)).to_csv(dir_path + rf"\Output\{col}_Stats_{date}.csv",index=True)

if __name__ == '__main__':
    path_to_data = dir_path + r"\Data\*.csv"
    for file in glob.glob(path_to_data):

        df = pd.read_csv(file)

        lists_of_ACE = df['Name'].apply(lambda x: x.split('\\'))

        dataframe_dict = {}
        for j in range(largestChain(df, 'Name')):
            dataframe_dict[j] = []

        for i in range(len(lists_of_ACE)):
            for j in range(largestChain(df, 'Name')):
                try:
                    dataframe_dict[j].append(lists_of_ACE[i][j])
                except Exception as e:
                    pass

        final_df = pd.DataFrame.from_dict(dataframe_dict,orient='index')
        final_df = final_df.T
        final_df = final_df.drop_duplicates().reset_index(drop=True)
        final_df = final_df[(final_df[1] == "ACE2xSchedulers") | (final_df[1] == "ACEClassLibraries")]

        final_df.columns = renameCols(final_df)
        date = str(datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"))
        final_df.to_csv(dir_path + fr"\Output\OverallAceOutput_{date}.csv",index=False)
        columnStats(final_df)



