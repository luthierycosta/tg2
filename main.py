import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, mutual_info_regression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
import csv_parser

# Parâmetros

INITIAL_YEAR = 2008
FINAL_YEAR = 2017
NOT_NAN_RATIO = 0.8
COUNTRIES_TO_DROP = 20

# Extração dos dados
df = csv_parser.get_dataframes(INITIAL_YEAR, FINAL_YEAR)
countries = csv_parser.get_metadata('Metadata_countries')
indicators = csv_parser.get_metadata('Metadata_series')

# Filtra países mantendo apenas os que constam no arquivo params.py
# df = df[df['Country Name'].isin(params.countries)]


# Dataframe que contabiliza a qtd. de valores vazios para cada indicador
# (apenas para fins ilustrativos/plotagem. Não é usado no processamento)
nan_per_indicator = pd.DataFrame(df.isna().sum()[3:]) \
    .rename(columns={0: 'Count'}) \
    .sort_values(by='Count',ascending=False)
nan_per_indicator['Name'] = indicators['Indicator Name']
#nan_per_indicator.plot()

# Filtra indicadores que possuem uma certa porcentagem de valores não-nulos
df = df.dropna(axis=1, thresh=NOT_NAN_RATIO*len(df))

# Dataframe que contabiliza a qtd. de valores vazios para cada país, somando os registros de todos os anos
nan_per_country = pd.DataFrame(
    sorted([
        [country, df[df['Country Name'] == country].isna().sum().sum()]
        for country in set(df['Country Name'])],
        key=lambda arr: arr[1], reverse=True
    ),
    columns=['Country Name', 'NaN values']
)

# Remove países que possuem mais valores vazios
df = df[~df['Country Name'].isin(nan_per_country.head(COUNTRIES_TO_DROP)['Country Name'])]




# Após filtragem de indicadores, remove todas as linhas que ainda conterem valores vazios
# Porque o RandomForest nao aceita valores vazios (não é capaz de interpolar)
#df = df.dropna(axis=0)

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
