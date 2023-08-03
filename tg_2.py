import os
import pandas as pd
import numpy as np


df2010 = pd.DataFrame()
base_folder = os.listdir('./data/2010')
for base_file in base_folder:
    if base_file.endswith('_Data.csv'):
        df2010 = pd.read_csv('./data/2010/' + base_file)
df2010 = df2010.drop(['Country Code', 'Series Name'], axis=1)
df2010 = df2010.rename(columns={'2010 [YR2010]': '2010'})
df2010['2010'] = df2010['2010'].replace('..', np.nan)
df2010['2010'] = pd.to_numeric(df2010['2010'])
df2010['Year'] = 2010
df2010_grouped = df2010.groupby(['Country Name', 'Year', 'Series Code'])['2010'].mean().reset_index()
df2010_pivot = df2010_grouped.pivot(index=['Country Name', 'Year'], columns='Series Code', values='2010').reset_index()
df2010_pivot.columns.name = None

df2011 = pd.DataFrame()
base_folder = os.listdir('./data/2011')
for base_file in base_folder:
    if base_file.endswith('_Data.csv'):
        df2011 = pd.read_csv('./data/2011/' + base_file)
df2011 = df2011.drop(['Country Code', 'Series Name'], axis=1)
df2011 = df2011.drop(df2011.tail(5).index)
df2011 = df2011.rename(columns={'2011 [YR2011]': '2011'})
df2011['2011'] = df2011['2011'].replace('..', np.nan)
df2011['2011'] = pd.to_numeric(df2011['2011'])
df2011['Year'] = 2011
df2011_grouped = df2011.groupby(['Country Name', 'Year', 'Series Code'])['2011'].mean().reset_index()
df2011_pivot = df2011_grouped.pivot(index=['Country Name', 'Year'], columns='Series Code', values='2011').reset_index()
df2011_pivot.columns.name = None


df2012 = pd.DataFrame()
base_folder = os.listdir('./data/2012')
for base_file in base_folder:
    if base_file.endswith('_Data.csv'):
        df2012 = pd.read_csv('./data/2012/' + base_file)
df2012 = df2012.drop(['Country Code', 'Series Name'], axis=1)
df2012 = df2012.drop(df2012.tail(5).index)
df2012 = df2012.rename(columns={'2012 [YR2012]': '2012'})
df2012['2012'] = df2012['2012'].replace('..', np.nan)
df2012['2012'] = pd.to_numeric(df2012['2012'])
df2012['Year'] = 2012
df2012_grouped = df2012.groupby(['Country Name', 'Year', 'Series Code'])['2012'].mean().reset_index()
df2012_pivot = df2012_grouped.pivot(index=['Country Name', 'Year'], columns='Series Code', values='2012').reset_index()
df2012_pivot.columns.name = None

df2013 = pd.DataFrame()
base_folder = os.listdir('./data/2013')
for base_file in base_folder:
    if base_file.endswith('_Data.csv'):
        df2013 = pd.read_csv('./data/2013/' + base_file)
df2013 = df2013.drop(['Country Code', 'Series Name'], axis=1)
df2013 = df2013.drop(df2013.tail(5).index)
df2013 = df2013.rename(columns={'2013 [YR2013]': '2013'})
df2013 = df2013.drop(df2013.tail(5).index)
df2013['2013'] = df2013['2013'].replace('..', np.nan)
df2013['2013'] = pd.to_numeric(df2013['2013'])
df2013['Year'] = 2013
df2013_grouped = df2013.groupby(['Country Name', 'Year', 'Series Code'])['2013'].mean().reset_index()
df2013_pivot = df2013_grouped.pivot(index=['Country Name', 'Year'], columns='Series Code', values='2013').reset_index()
df2013_pivot.columns.name = None

df2014 = pd.DataFrame()
base_folder = os.listdir('./data/2014')
for base_file in base_folder:
    if base_file.endswith('_Data.csv'):
        df2014 = pd.read_csv('./data/2014/' + base_file)
df2014 = df2014.drop(['Country Code', 'Series Name'], axis=1)
df2014 = df2014.drop(df2014.tail(5).index)
df2014 = df2014.rename(columns={'2014 [YR2014]': '2014'})
df2014['2014'] = df2014['2014'].replace('..', np.nan)
df2014['2014'] = pd.to_numeric(df2014['2014'])
df2014['Year'] = 2014
df2014_grouped = df2014.groupby(['Country Name', 'Year', 'Series Code'])['2014'].mean().reset_index()
df2014_pivot = df2014_grouped.pivot(index=['Country Name', 'Year'], columns='Series Code', values='2014').reset_index()
df2014_pivot.columns.name = None

df2015 = pd.DataFrame()
base_folder = os.listdir('./data/2015')
for base_file in base_folder:
    if base_file.endswith('_Data.csv'):
        df2015 = pd.read_csv('./data/2015/' + base_file)
df2015 = df2015.drop(['Country Code', 'Series Name'], axis=1)
df2015 = df2015.drop(df2015.tail(5).index)
df2015 = df2015.rename(columns={'2015 [YR2015]': '2015'})
df2015['2015'] = df2015['2015'].replace('..', np.nan)
df2015['2015'] = pd.to_numeric(df2015['2015'])
df2015['Year'] = 2015
df2015_grouped = df2015.groupby(['Country Name', 'Year', 'Series Code'])['2015'].mean().reset_index()
df2015_pivot = df2015_grouped.pivot(index=['Country Name', 'Year'], columns='Series Code', values='2015').reset_index()
df2015_pivot.columns.name = None

df2016 = pd.DataFrame()
base_folder = os.listdir('./data/2016')
for base_file in base_folder:
    if base_file.endswith('_Data.csv'):
        df2016 = pd.read_csv('./data/2016/' + base_file)
df2016 = df2016.drop(['Country Code', 'Series Name'], axis=1)
df2016 = df2016.drop(df2016.tail(5).index)
df2016 = df2016.rename(columns={'2016 [YR2016]': '2016'})
df2016['2016'] = df2016['2016'].replace('..', np.nan)
df2016['2016'] = pd.to_numeric(df2016['2016'])
df2016['Year'] = 2016
df2016_grouped = df2016.groupby(['Country Name', 'Year', 'Series Code'])['2016'].mean().reset_index()
df2016_pivot = df2016_grouped.pivot(index=['Country Name', 'Year'], columns='Series Code', values='2016').reset_index()
df2016_pivot.columns.name = None

df2017 = pd.DataFrame()
base_folder = os.listdir('./data/2017')
for base_file in base_folder:
    if base_file.endswith('_Data.csv'):
        df2017 = pd.read_csv('./data/2017/' + base_file)
df2017 = df2017.drop(['Country Code', 'Series Name'], axis=1)
df2017 = df2017.drop(df2017.tail(5).index)
df2017 = df2017.rename(columns={'2017 [YR2017]': '2017'})
df2017['2017'] = df2017['2017'].replace('..', np.nan)
df2017['2017'] = pd.to_numeric(df2017['2017'])
df2017['Year'] = 2017
df2017_grouped = df2017.groupby(['Country Name', 'Year', 'Series Code'])['2017'].mean().reset_index()
df2017_pivot = df2017_grouped.pivot(index=['Country Name', 'Year'], columns='Series Code', values='2017').reset_index()
df2017_pivot.columns.name = None

df2018 = pd.DataFrame()
base_folder = os.listdir('./data/2018')
for base_file in base_folder:
    if base_file.endswith('_Data.csv'):
        df2018 = pd.read_csv('./data/2018/' + base_file)
df2018 = df2018.drop(['Country Code', 'Series Name'], axis=1)
df2018 = df2018.drop(df2018.tail(5).index)
df2018 = df2018.rename(columns={'2018 [YR2018]': '2018'})
df2018['2018'] = df2018['2018'].replace('..', np.nan)
df2018['2018'] = pd.to_numeric(df2018['2018'])
df2018['Year'] = 2018
df2018_grouped = df2018.groupby(['Country Name', 'Year', 'Series Code'])['2018'].mean().reset_index()
df2018_pivot = df2018_grouped.pivot(index=['Country Name', 'Year'], columns='Series Code', values='2018').reset_index()
df2018_pivot.columns.name = None

df2019 = pd.DataFrame()
base_folder = os.listdir('./data/2019')
for base_file in base_folder:
    if base_file.endswith('_Data.csv'):
        df2019 = pd.read_csv('./data/2019/' + base_file)
df2019 = df2019.drop(['Country Code', 'Series Name'], axis=1)
df2019 = df2019.drop(df2019.tail(5).index)
df2019 = df2019.rename(columns={'2019 [YR2019]': '2019'})
df2019['2019'] = df2019['2019'].replace('..', np.nan)
df2019['2019'] = pd.to_numeric(df2019['2019'])
df2019['Year'] = 2019
df2019_grouped = df2019.groupby(['Country Name', 'Year', 'Series Code'])['2019'].mean().reset_index()
df2019_pivot = df2019_grouped.pivot(index=['Country Name', 'Year'], columns='Series Code', values='2019').reset_index()
df2019_pivot.columns.name = None

df2020 = pd.DataFrame()
base_folder = os.listdir('./data/2020')
for base_file in base_folder:
    if base_file.endswith('_Data.csv'):
        df2020 = pd.read_csv('./data/2020/' + base_file)
df2020 = df2020.drop(['Country Code', 'Series Name'], axis=1)
df2020 = df2020.drop(df2020.tail(5).index)
df2020 = df2020.rename(columns={'2020 [YR2020]': '2020'})
df2020['2020'] = df2020['2020'].replace('..', np.nan)
df2020['2020'] = pd.to_numeric(df2020['2020'])
df2020['Year'] = 2020
df2020_grouped = df2020.groupby(['Country Name', 'Year', 'Series Code'])['2020'].mean().reset_index()
df2020_pivot = df2020_grouped.pivot(index=['Country Name', 'Year'], columns='Series Code', values='2020').reset_index()
df2020_pivot.columns.name = None

df2021 = pd.DataFrame()
base_folder = os.listdir('./data/2021')
for base_file in base_folder:
    if base_file.endswith('_Data.csv'):
        df2021 = pd.read_csv('./data/2021/' + base_file)
df_hash = df2021[['Series Name', 'Series Code']]
df2021 = df2021.drop(['Country Code', 'Series Name'], axis=1)
df2021 = df2021.drop(df2021.tail(5).index)
df2021 = df2021.rename(columns={'2021 [YR2021]': '2021'})
df2021['2021'] = df2021['2021'].replace('..', np.nan)
df2021['2021'] = pd.to_numeric(df2021['2021'])
df2021['Year'] = 2021
df2021_grouped = df2021.groupby(['Country Name', 'Year', 'Series Code'])['2021'].mean().reset_index()
df2021_pivot = df2021_grouped.pivot(index=['Country Name', 'Year'], columns='Series Code', values='2021').reset_index()
df2021_pivot.columns.name = None

pdList = [df2010_pivot, df2011_pivot, df2012_pivot, df2013_pivot, df2014_pivot, df2015_pivot, df2016_pivot, df2017_pivot, df2018_pivot, df2019_pivot, df2020_pivot, df2021_pivot]
new_df = pd.concat(pdList)

final_dataframe = new_df.sort_values(by=['Country Name', 'Year'], ascending=[True, False])

# Salvar em um arquivo CSV
final_dataframe.to_csv('dataframe_series_code.csv', index=False)  # Define index=False para não incluir o índice no arquivo CSV

# Criar um novo DataFrame com as colunas "Series Name" e "Series Code"

# Remover valores duplicados
df_hash = df_hash.drop_duplicates()

# Salvar em um arquivo CSV
df_hash.to_csv('map_series_code.csv', index=False)  # Define index=False para não incluir o índice no arquivo CSV
