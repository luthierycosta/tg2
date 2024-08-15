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

DATAFRAMES_PATH = './dataframes/'
TABLES_PATH = './dataframes/incluir_no_tcc_como_tabelas/'

MAIN_DF_PATH = DATAFRAMES_PATH + 'WDItratado.csv'
RAW_DF_PATH = DATAFRAMES_PATH + 'WDICSV.csv'
COUNTRIES_PATH = DATAFRAMES_PATH + 'WDICountry.csv'
INDICATORS_PATH = DATAFRAMES_PATH + 'WDISeries.csv'


YEARS_TO_DROP = 16      # 1/4 do total de anos
COUNTRIES_TO_DROP = 28  # aprox. 10% dos 266 países
NOT_NAN_FILTER = 0.6   # exclui todo indicador com + de 40% valores nulos
TEST_SET_RATIO = 0.25
FEATURES_TO_SELECT = 20

### Extração dos dados

wdi = pd.read_csv(MAIN_DF_PATH)
raw_wdi = pd.read_csv(RAW_DF_PATH)
countries = pd.read_csv(COUNTRIES_PATH, index_col='Country Code')
indicators = pd.read_csv(INDICATORS_PATH, index_col='Series Code')


### Variáveis para análise sobre o dataset inicial

total_indicators = len(indicators)
total_countries = len(countries)
total_years = len(wdi.groupby('Year'))
total_nan = wdi.isna().sum().sum()
total_values = total_countries * total_indicators * total_years

# Dataframe que mostra a qtd. de valores vazios para cada indicador
nan_per_indicator = wdi.isna().sum()[3:] \
    .to_frame().rename(columns={0: 'NaN values'})
nan_per_indicator.insert(0, 'Name', indicators['Indicator Name'])
nan_per_indicator.insert(2, 'Percentage', (nan_per_indicator['NaN values'] / len(wdi) * 100).round(2))

# Série que mostra a qtd. de valores vazios por ano, somando todos os países e indicadores
nan_per_year = raw_wdi.isna().sum()[4:]

# Série que mostra a qtd. de valores vazios para cada país, somando todos os anos
nan_per_country = wdi.groupby(['Country Code', 'Country Name']) \
    .count() \
    .drop(columns='Year') \
    .sum(axis=1) \
    .apply(lambda x: total_indicators * total_years - x) \
    .to_frame('NaN values') \
    .reset_index()

    
### Criação de gráficos e tabelas para análise sobre o dataset inicial

nan_per_indicator['NaN values'].plot.hist(
    xlabel='Qtd. de valores nulos',
    ylabel='Frequência dos indicadores',
    bins=20,
    grid=True)
nan_per_year.plot(
    xlabel='Ano',
    ylabel='Valores nulos',
    ylim=(0, 400000),
    grid=True)


### Pré-processamento

emptiest_indicators = nan_per_indicator.nlargest(50, 'NaN values')
emptiest_years = nan_per_year.nlargest(YEARS_TO_DROP)
emptiest_countries = nan_per_country.nlargest(COUNTRIES_TO_DROP, 'NaN values')


# Exlui registros que possuem a variável "crescimento do PIB" (o alvo do modelo) vazia
[gdp_growth_code] = indicators.query("`Indicator Name` == 'GDP growth (annual %)'").index
wdi = wdi.dropna(subset=[gdp_growth_code])

# Remove os anos que possuem mais valores vazios, conforme parâmetro
wdi = wdi[~wdi['Year'].isin(emptiest_years.index.astype(int))]

# Remove os países que possuem mais valores vazios, conforme parâmetro
wdi = wdi[~wdi['Country Code'].isin(emptiest_countries['Country Code'])]

# Mantém apenas indicadores que possuem uma porcentagem de valores não-nulos, conforme parâmetro
wdi = wdi.dropna(axis=1, thresh=NOT_NAN_FILTER*len(wdi))




### Processamento dos conjuntos de teste e treinamento

# TODO: REMOVER ESSES INDICADORES DO CONJUNTO DE TREINAMENTO
gdp_indicators = indicators[indicators['Indicator Name'].str.contains("GDP")]
gni_indicators = indicators[indicators['Indicator Name'].str.contains("GNI")]

gdp_indicators.to_csv(DATAFRAMES_PATH + 'IndicadoresPIB.csv', columns=['Indicator Name'])

# Separa as variáveis de entrada (X) e variável alvo (y)
# e remove as variáveis relacionadas ao PIB
X = wdi.drop(columns=['Country Name', 'Country Code', 'Year'])
y = wdi[gdp_growth_code]

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
