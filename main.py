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
# df = df[df['Country Name'].isin(params.countries)]

# Dataframe/Gráfico que contabiliza a quantidade de valores vazios para cada indicador
"""
count_nan = df.isna().sum()[3:]
count_nan = count_nan.to_frame() \
    .rename(columns={0: 'Count'}) \
    .sort_values(by='Count',ascending=False)
count_nan['Series Name'] = pd.Series(indicator_names)
count_nan.plot()
"""

# Filtra indicadores que possuem uma certa porcentagem de valores não-nulos
filtered_df = df.dropna(axis=1, thresh=params.thresh*len(df))


# Dataframe/Gráfico que mostra a média de indicadores vazios por país, para cada ano
"""
na_per_year = {
    year: df[df['Year'] == year].isna().sum(axis=1).median() \
    for year in set(df['Year'])
}
na_per_year = pd.DataFrame.from_dict(na_per_year,orient='index')
na_per_year.plot()
"""
