import os
import pandas as pd
import numpy as np


finalData = pd.DataFrame()

for i in range(2008, 2012+1):

    year = str(i)
    
    folder = './Data_extracts/' + year
    [filename] = [file for file in os.listdir(folder) if file.endswith('_Data.csv')]
    data = pd.read_csv(
        folder+'/'+filename,
        usecols = lambda col: col != 'Series Name',
        na_values = '..'
    )
    
    data = data[:-5]
    data = data.rename(columns={f'{year} [YR{year}]' : year})
    
    data['Year'] = i
    
    data = data.pivot(index=['Country Name', 'Country Code', 'Year'], columns='Series Code', values=year)
    newColumns = data.columns.difference(finalData.columns)
    

    finalData = pd.concat([finalData, data[newColumns]], axis=1)

    #temp = pd.read_csv('./Data_extracts/'+year+'/'+r'{*}_Data.csv')

finalData = finalData.sort_values(['Country Code', 'Year'])



#print(os.listdir('./Data_extracts/2008'))
#newData = mergeDataframe(2008,2012)
