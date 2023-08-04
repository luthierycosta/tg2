import pandas as pd
import numpy as np
from os import listdir


dataframes = []

for y in range(2008, 2022+1):

    year = str(y)
    
    folder = './Data_extracts/' + year
    [filename] = [file for file in listdir(folder) if file.endswith('_Data.csv')]
    data = pd.read_csv(
        folder+'/'+filename,
        usecols = lambda col: col != 'Series Name',
        na_values = '..'
    )
    
    data = data[:-5]
    data = data.rename(columns={f'{year} [YR{year}]' : year})
    
    data['Year'] = y
    
    data = data.pivot(index=['Country Name', 'Country Code', 'Year'], columns='Series Code', values=year)
    dataframes.append(data)

finalData = pd.concat(dataframes).sort_values(['Country Code', 'Year']).reset_index()

# newColumns = data.columns.difference(finalData.columns)
    
# tempData = pd.concat([tempData, data], axis=1)
# finalData = pd.concat([finalData, data[newColumns]], axis=1)

    #temp = pd.read_csv('./Data_extracts/'+year+'/'+r'{*}_Data.csv')



#print(listdir('./Data_extracts/2008'))
#newData = mergeDataframe(2008,2012)
