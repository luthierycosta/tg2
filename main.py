import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, mutual_info_regression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
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
df = df.dropna(axis=1, thresh=params.thresh*len(df))

# Após filtragem de indicadores, remove todas as linhas que ainda conterem valores vazios
# Porque nao sei usar o HistBoost sla oq
df = df.dropna(axis=0)

# Dataframe/Gráfico que mostra a média de indicadores vazios por país, para cada ano
"""
na_per_year = {
    year: df[df['Year'] == year].isna().sum(axis=1).median() \
    for year in set(df['Year'])
}
na_per_year = pd.DataFrame.from_dict(na_per_year,orient='index')
na_per_year.plot()
"""

X = df.drop(columns=['Country Name','Country Code','Year','NY.GDP.MKTP.KD.ZG'])
y = df['NY.GDP.MKTP.KD.ZG']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Select the top 3 most informative features using mutual information
feature_selector = SelectKBest(mutual_info_regression, k=3)
X_selected = feature_selector.fit_transform(X_scaled, y)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2)

# Train a Random Forest Regressor model on the training data
model = RandomForestRegressor()
model.fit(X_train, y_train)

result = model.score(X_test, y_test)
print (f'result: {result:.2f}')