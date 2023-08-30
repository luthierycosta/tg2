import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
import csv_parser
import params

df = csv_parser.get_dataframes(params.initial_year, params.final_year)
countries = csv_parser.get_metadata('Metadata_countries')
indicators = csv_parser.get_metadata('Metadata_series')

country_names = dict(countries['Table Name'])
indicator_names = dict(indicators['Indicator Name'])

# Filtra países mantendo apenas os que constam no arquivo params.py
df = df[df['Country Name'].isin(params.countries)]

count_nan = df.isna().sum()[3:]

count_nan_df = count_nan.to_frame() \
    .rename(columns={0: 'Count'}) \
    .sort_values(by='Count',ascending=False) \
    .reset_index()


count_nan_df['Series Name'] = pd.Series(indicator_names)

# Gráfico que mostra o total de valores vazios pra cada indicador, considerando todos os registros
count_nan_df.plot()

#Filtra indicadores que possuem mais de 80% de valores não-nulos e remove todo o resto
filtered_df = df.dropna(axis=1, thresh=params.thresh*len(df))

na_per_year = {}
for year in range(params.initial_year, params.final_year+1):
    na_per_year[year] = df[df['Year'] == year].isna().sum(axis=1).median()
    
# Gráfico que mostra a média de valores vazios por país, para cada ano
peryear_df = pd.DataFrame.from_dict(na_per_year,orient='index')
peryear_df.plot()
