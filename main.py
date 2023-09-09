""" O projeto em si. Usa o framework Pandas para mineração de dados dos indicadores do WorldBank.
"""
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, mutual_info_regression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor, HistGradientBoostingRegressor
from sklearn.impute import KNNImputer
import csv_parser

### Parâmetros

INITIAL_YEAR = 2009
FINAL_YEAR = 2018
NOT_NAN_FILTER = 0.85
COUNTRIES_TO_DROP = 20
TEST_SET_RATIO = 0.25
FEATURES_TO_SELECT = 20

### Extração dos dados

df = csv_parser.get_dataframes(INITIAL_YEAR, FINAL_YEAR)
countries = csv_parser.get_metadata('Metadata_countries')
indicators = csv_parser.get_metadata('Metadata_series')

### Dataframes e gráficos para ilustração sobre o dataset inicial

# Dataframe que mostra a qtd. de valores vazios para cada indicador
nan_per_indicator = pd.DataFrame(df.isna().sum()[3:]) \
    .rename(columns={0: 'NaN values'}) \
    .sort_values(by='NaN values',ascending=False)
nan_per_indicator['Name'] = indicators['Indicator Name']
#nan_per_indicator.plot()

# Dataframe que mostra a qtd. de valores vazios por ano, contando todos os países
nan_per_year = sorted(
    [[year, df[df['Year'] == year].isna().sum().sum()]
    for year in set(df['Year'])],
    key=lambda arr: arr[0])
nan_per_year = pd.DataFrame(nan_per_year, columns=['Year', 'NaN values'])
nan_per_year.plot()

# Dataframe que mostra a qtd. de valores vazios para cada país, somando todos os anos
nan_per_country = sorted([
    [country, df[df['Country Name'] == country].isna().sum().sum()]
    for country in set(df['Country Name'])],
    key=lambda arr: arr[1], reverse=True)
nan_per_country = pd.DataFrame(nan_per_country, columns=['Country Name', 'NaN values'])
#nan_per_country.plot()

### Pré-processamento

# Remove os países que possuem mais valores vazios, conforme parâmetro
df = df[~df['Country Name'].isin(nan_per_country.head(COUNTRIES_TO_DROP)['Country Name'])]

# Mantém apenas indicadores que possuem uma porcentagem de valores não-nulos, conforme parâmetro
df = df.dropna(axis=1, thresh=NOT_NAN_FILTER*len(df))

# Exlui registros que possuem a variável "crescimento do PIB" (o alvo do modelo) vazia
[gdp_growth_code] = indicators.query("`Indicator Name` == 'GDP growth (annual %)'").index
df = df.dropna(subset=[gdp_growth_code])

### Processamento dos conjuntos de teste e treinamento

# Separa as variáveis de entrada (X) e variável alvo (y)    
X = df.drop(columns=['Country Name','Country Code','Year'])
y = df[gdp_growth_code]

# Normaliza o conjunto de entrada
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X, y)

# Preenche os valores vazios no conjunto de entrada
imputer = KNNImputer(n_neighbors=5, weights='uniform')
X_imputed = imputer.fit_transform(X_scaled)

# Separa em conjuntos de teste e treinamento
X_train, X_test, y_train, y_test = train_test_split(X_imputed, y, test_size=TEST_SET_RATIO, random_state=0)

# Filtra os melhores indicadores, conforme parâmetro 
feature_selector = SelectKBest(mutual_info_regression, k=FEATURES_TO_SELECT)
feature_selector.fit_transform(X_train, y_train)
X_train_selected = feature_selector.transform(X_train)
X_test_selected = feature_selector.transform(X_test)


### Aplicação dos modelos 

random_forest = RandomForestRegressor(random_state=0)
random_forest.fit(X_train_selected, y_train)

gradient_boosting = HistGradientBoostingRegressor(random_state=0)
gradient_boosting.fit(X_train_selected, y_train)

scores = (
    random_forest.score(X_test_selected, y_test),
    gradient_boosting.score(X_test_selected, y_test)
)
