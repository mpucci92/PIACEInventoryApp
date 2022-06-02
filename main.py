import pandas as pd
import numpy as np
import os
import glob as glob

dir_path = os.path.dirname(os.path.realpath(__file__))
path_to_data = dir_path + r"\Data\*.csv"

for file in glob.glob(path_to_data):
    df = pd.read_csv(file)

    df = df[df['Name'].str.contains("ACEClassLibraries")].reset_index(drop=True)

    module_df = df[df['Type'] == "Module"]
    module_df = module_df.reset_index(drop=True)

    moduleNameList = []

    for i in range(len(module_df['Name'])):
        module_df['Name'].apply(lambda x: x.split("\\"))[i]
        filterIndex = module_df['Name'].apply(lambda x: x.split("\\"))[i].index("ACEClassLibraries")
        moduleName = "\\".join(module_df['Name'].apply(lambda x: x.split("\\"))[i][filterIndex:])
        moduleNameList.append(moduleName)

    module_df['ModuleName'] = moduleNameList
    module_df = module_df.loc[:, ['Name', 'Type', 'ModuleName', 'ModuleCreator']]
    module_df.columns = ['FullPath', 'Type', 'ModuleName', 'ModuleCreator']

    df.rename(columns={'Name': 'FullPath'}, inplace=True)

    ModuleIndexes = []

    for i in range(len(module_df)):
        ModuleIndexes.append(list(df['FullPath']).index(module_df['FullPath'][i]))

    DataframeList = []

    for i in range(len(ModuleIndexes)):
        propertyList = []
        try:
            tmp = df.loc[ModuleIndexes[i]:ModuleIndexes[i + 1] - 1, :]

            tmp = tmp.loc[:, ['FullPath', 'Type', 'PropertyValue']]

            for j in range(len(tmp)):
                try:
                    propertyList.append(list(tmp['FullPath'].apply(lambda x: x.split("||")))[j][1])
                except Exception as e:
                    propertyList.append(None)
                    continue

            tmp['PropertyName'] = propertyList
            final = tmp.loc[:, ['FullPath', 'Type', 'PropertyName', 'PropertyValue']]
            DataframeList.append(final)
        except Exception as e:
            tmp = df.loc[ModuleIndexes[i]:, :]
            tmp = tmp.loc[:, ['FullPath', 'Type', 'PropertyValue']]

            for j in range(len(tmp)):
                try:
                    propertyList.append(list(tmp['FullPath'].apply(lambda x: x.split("||")))[j][1])
                except Exception as e:
                    propertyList.append(None)
                    continue

            tmp['PropertyName'] = propertyList
            final = tmp.loc[:, ['FullPath', 'Type', 'PropertyName', 'PropertyValue']]
            DataframeList.append(final)

    ModuleDictionary = {}

    for i, name in enumerate(module_df['ModuleName']):
        ModuleDictionary[i] = name

    for i in range(len(DataframeList)):
        csvName = ModuleDictionary[i].replace("\\", "-")
        DataframeList[i].to_csv(dir_path + fr"\Output\{csvName}.csv",
                                index=False)

    df_empty = pd.DataFrame()
    for i, value in enumerate(DataframeList):
        if i == 0:
            complete_df = pd.concat([df_empty, value], axis=0)
        else:
            complete_df = pd.concat([complete_df, value], axis=0)

    complete_df.to_csv(dir_path + fr"\Output\COMPLETE.csv", index=False)
