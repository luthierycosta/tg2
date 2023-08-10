import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv_parser

df = csv_parser.get_dataframes(2008, 2018)
countries = csv_parser.get_countries_metadata()
indicators = csv_parser.get_indicators_metadata()

country_names = dict(countries['Table Name'])
indicator_names = dict(indicators['Indicator Name'])

count_nan = df.isna().sum()[3:]

count_nan_df = count_nan.to_frame() \
    .rename(columns={0: 'Count'}) \
    .sort_values(by='Count',ascending=False) \
    .reset_index()


count_nan_df['Series Name'] = pd.Series(indicator_names)

# Gráfico que mostra o total de valores vazios pra cada indicador, considerando todos os registros
count_nan_df.plot()

#Filtra indicadores que possuem mais de 80% de valores não-nulos e remove todo o resto
filtered_df = df.dropna(axis=1, thresh=0.8*len(df))

na_per_year = {}
for year in range(2008, 2023):
    na_per_year[year] = df[df['Year'] == year].isna().sum(axis=1).median()
    
# Gráfico que mostra a média de valores vazios por país, para cada ano
peryear_df = pd.DataFrame.from_dict(na_per_year,orient='index')
peryear_df.plot()
