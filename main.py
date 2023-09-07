import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, mutual_info_regression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import csv_parser

### Parâmetros

INITIAL_YEAR = 2008
FINAL_YEAR = 2017
NOT_NAN_RATIO = 0.8
COUNTRIES_TO_DROP = 20

### Extração dos dados
df = csv_parser.get_dataframes(INITIAL_YEAR, FINAL_YEAR)
countries = csv_parser.get_metadata('Metadata_countries')
indicators = csv_parser.get_metadata('Metadata_series')

### Dataframes e gráficos para ilustração

# Dataframe que mostra a qtd. de valores vazios para cada indicador
nan_per_indicator = pd.DataFrame(df.isna().sum()[3:]) \
    .rename(columns={0: 'NaN values'}) \
    .sort_values(by='NaN values',ascending=False)
nan_per_indicator['Name'] = indicators['Indicator Name']
#nan_per_indicator.plot()

# Dataframe que mostra a qtd. de indicadores vazios por ano, somando todos os países
nan_per_year = sorted(
    [[year, df[df['Year'] == year].isna().sum(axis=1).mean()]
    for year in set(df['Year'])],
    key=lambda arr: arr[0])
nan_per_year = pd.DataFrame(nan_per_year, columns=['Year', 'NaN values'])
#nan_per_year.plot()

# Dataframe que mostra a qtd. de valores vazios para cada país, somando todos os anos
nan_per_country = sorted([
    [country, df[df['Country Name'] == country].isna().sum().sum()]
    for country in set(df['Country Name'])],
    key=lambda arr: arr[1], reverse=True)
nan_per_country = pd.DataFrame(nan_per_country, columns=['Country Name', 'NaN values'])
#nan_per_country.plot()


### Pré-processamento

# Mantém apenas indicadores que possuem uma porcentagem de valores não-nulos, conforme parâmetro
df = df.dropna(axis=1, thresh=NOT_NAN_RATIO*len(df))


# Remove os países que possuem mais valores vazios, conforme parâmetro
df = df[~df['Country Name'].isin(nan_per_country.head(COUNTRIES_TO_DROP)['Country Name'])]




# Após filtragem de indicadores, remove todas as linhas que ainda conterem valores vazios
# Porque o RandomForest nao aceita valores vazios (não é capaz de interpolar)
#df = df.dropna(axis=0)





X = df.drop(columns=['Country Name','Country Code','Year','NY.GDP.MKTP.KD.ZG'])
y = df['NY.GDP.MKTP.KD.ZG']

X_scaled = StandardScaler().fit_transform(X)

# Select the top 3 most informative features using mutual information
feature_selector = SelectKBest(mutual_info_regression, k=20)
X_selected = feature_selector.fit_transform(X_scaled, y)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2)

# Train a Random Forest Regressor model on the training data
model = RandomForestRegressor()
model.fit(X_train, y_train)

result = model.score(X_test, y_test)
print (f'result: {result:.2f}')
