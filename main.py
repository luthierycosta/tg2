import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv_parser

df = csv_parser.get_dataframes(2008, 2018)
countries_metadata = csv_parser.get_countries_metadata()
series_metadata = csv_parser.get_series_metadata()

count_nan = df.isna().sum()[3:]

count_nan_df = count_nan.to_frame().rename(columns={0: 'Count'}).sort_values(by='Count').reset_index()


count_nan_df['Series Name'] = pd.Series(series_metadata)

# Gráfico que mostra o total de valores vazios pra cada indicador, considerando todos os registros
#count_nan_df.plot()

filtered_df = df.dropna(axis=1, thresh=count_nan.median())

na_per_year = {}
for year in range(2008, 2023):
    na_per_year[year] = df[df['Year'] == year].isna().sum(axis=1).median()
    
# Gráfico que mostra a média de valores vazios por país, para cada ano
peryear_df = pd.DataFrame.from_dict(na_per_year,orient='index')
peryear_df.plot()
