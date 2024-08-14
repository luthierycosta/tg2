""" O projeto em si. Usa o framework Pandas para mineração de dados dos indicadores do WorldBank.
"""
import numpy as np
import pandas as pd
import matplotlib as mpl
import matplotlib.pyplot as plt
# from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, r_regression, mutual_info_regression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import KNNImputer

### Parâmetros

WORKSPACE_PATH = './dataframes/'
MAIN_DF_PATH = WORKSPACE_PATH + 'WDItratado.csv'
RAW_DF_PATH = WORKSPACE_PATH + 'WDICSV.csv'
COUNTRIES_PATH = WORKSPACE_PATH + 'WDICountry.csv'
INDICATORS_RESUMED_PATH = WORKSPACE_PATH + 'WDISeriesResumed.csv'
INDICATORS_PATH = WORKSPACE_PATH + 'WDISeries.csv'

NOT_NAN_FILTER = 0.7
COUNTRIES_TO_DROP = 28
YEARS_TO_DROP = 16
TEST_SET_RATIO = 0.25
FEATURES_TO_SELECT = 20

### Extração dos dados

df = pd.read_csv(MAIN_DF_PATH)
raw_df = pd.read_csv(RAW_DF_PATH)
countries = pd.read_csv(COUNTRIES_PATH, index_col='Country Code')
indicators = pd.read_csv(INDICATORS_PATH, index_col='Series Code')
indicators.to_csv(INDICATORS_RESUMED_PATH, columns=['Indicator Name'])


### Variáveis para análise sobre o dataset inicial

total_nan = df.isna().sum()
total_indicators = len(df.columns) - 3
total_years = len(df.groupby('Year'))

# Dataframe que mostra a qtd. de valores vazios para cada indicador
nan_per_indicator = df.isna().sum()[3:] \
    .to_frame().rename(columns={0: 'NaN values'})
nan_per_indicator.insert(0, 'Name', indicators['Indicator Name'])

# Série que mostra a qtd. de valores vazios por ano, somando todos os países e indicadores
nan_per_year = raw_df.isna().sum()[4:]

# Série que mostra a qtd. de valores vazios para cada país, somando todos os anos
nan_per_country = df.groupby(['Country Code', 'Country Name']) \
    .count() \
    .drop(columns='Year') \
    .sum(axis=1) \
    .apply(lambda x: total_indicators * total_years - x)

    
### Plotagem de gráficos para análise sobre o dataset inicial

# nan_per_indicator.plot()
nan_per_year.plot(xlabel='Year', ylim=(0, 400000))

### Pré-processamento

# Remove os anos que possuem mais valores vazios, conforme parâmetro
df = df[~df['Year'].isin(nan_per_year.nlargest(YEARS_TO_DROP).index.astype(int))]

# Remove os países que possuem mais valores vazios, conforme parâmetro
df = df[~df['Country Name'].isin(nan_per_country.head(COUNTRIES_TO_DROP)['Country Name'])]

# Mantém apenas indicadores que possuem uma porcentagem de valores não-nulos, conforme parâmetro
df = df.dropna(axis=1, thresh=NOT_NAN_FILTER*len(df))

# Exlui registros que possuem a variável "crescimento do PIB" (o alvo do modelo) vazia
[gdp_growth_code] = indicators.query("`Indicator Name` == 'GDP growth (annual %)'").index
df = df.dropna(subset=[gdp_growth_code])


### Processamento dos conjuntos de teste e treinamento

# TODO: REMOVER ESSES INDICADORES DO CONJUNTO DE TREINAMENTO
gdp_indicators = indicators[indicators['Indicator Name'].str.contains("GDP")]
gni_indicators = indicators[indicators['Indicator Name'].str.contains("GNI")]

gdp_indicators.to_csv(WORKSPACE_PATH + 'GDPindicators.csv', columns=['Indicator Name'])

# Separa as variáveis de entrada (X) e variável alvo (y)
# e remove as variáveis relacionadas ao PIB
X = df.drop(columns=['Country Name', 'Country Code', 'Year'])
y = df[gdp_growth_code]

# Normaliza o conjunto de entrada
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X, y)

# Preenche os valores vazios no conjunto de entrada
imputer = KNNImputer(n_neighbors=5, weights='uniform')
X_imputed = imputer.fit_transform(X)

# Separa em conjuntos de teste e treinamento
X_train, X_test, y_train, y_test = train_test_split(
    X_imputed, y, test_size=TEST_SET_RATIO, random_state=0)

# Filtra os melhores indicadores, conforme parâmetro
feature_selector = SelectKBest(r_regression, k=FEATURES_TO_SELECT)
feature_selector.fit_transform(X_train, y_train)
X_train_selected = feature_selector.transform(X_train)
X_test_selected = feature_selector.transform(X_test)


### Aplicação dos modelos

random_forest = RandomForestRegressor(random_state=0)
random_forest.fit(X_train_selected, y_train)

score = random_forest.score(X_test_selected, y_test)
