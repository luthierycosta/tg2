""" Passo 3: realiza a modelagem com Scikit-Learn a partir da base de dados tratada nos passos anteriores.
"""
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_selection import SelectKBest, r_regression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import KNNImputer

### Constantes de ambiente

DATAFRAMES_PATH = './dataframes/'
TABLES_PATH = './material_overleaf/tabelas/'

TRANSFORMED_DF_PATH = DATAFRAMES_PATH + 'WDItransformada.csv'
PREPROCESSED_DF_PATH = DATAFRAMES_PATH + 'WDIPreProcessada.csv'
RAW_DF_PATH = DATAFRAMES_PATH + 'WDICSV.csv'
COUNTRIES_PATH = DATAFRAMES_PATH + 'WDICountry.csv'
INDICATORS_PATH = DATAFRAMES_PATH + 'WDISeries.csv'


### Parâmetros

KNN_IMPUTER_NEIGHBOURS = 10
TEST_SET_RATIO = 0.25
FEATURES_TO_SELECT = 32


### Extração dos dados

wdi = pd.read_csv(PREPROCESSED_DF_PATH)
transformed_wdi = pd.read_csv(TRANSFORMED_DF_PATH)
raw_wdi = pd.read_csv(RAW_DF_PATH)
countries = pd.read_csv(COUNTRIES_PATH, index_col='Country Code')
indicators = pd.read_csv(INDICATORS_PATH, index_col='Series Code')


### Separa as variáveis de entrada (X) e variável alvo (y)

[gdp_growth_code] = indicators.query("`Indicator Name` == 'GDP growth (annual %)'").index
wdi = wdi.set_index(['Country Name', 'Country Code', 'Year'])
X = wdi.drop(columns=[gdp_growth_code])
y = wdi[gdp_growth_code]

# Normaliza o conjunto de entrada
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X, y)

# Preenche os valores vazios no conjunto de entrada por inferência

imputer = KNNImputer(n_neighbors=KNN_IMPUTER_NEIGHBOURS, weights='uniform')
X_imputed = imputer.fit_transform(X)
X_imputed = pd.DataFrame(X_imputed, columns=X.columns, index=X.index)



### Separa em conjuntos de teste e treinamento

X_train, X_test, y_train, y_test = train_test_split(
    X_imputed, y, test_size=TEST_SET_RATIO, random_state=200)


### Remove indicadores enviesados

biased_indicators = indicators[indicators['Indicator Name'].str.contains('growth')]
# biased_indicators = indicators[indicators.index.str.contains('GDP')]

X_train = X_train.drop(columns=[c for c in biased_indicators.index if c in X_train.columns])
X_test = X_test.drop(columns=[c for c in biased_indicators.index if c in X_test.columns])


### Seleciona os melhores indicadores, conforme parâmetro


feature_selector = SelectKBest(r_regression, k=FEATURES_TO_SELECT)
feature_selector.fit(X_train, y_train)
X_train_selected = pd.DataFrame(
    feature_selector.transform(X_train),
    columns = X_train.columns[feature_selector.get_support()],
    index = X_train.index)
X_test_selected = pd.DataFrame(
    feature_selector.transform(X_test),
    columns = X_test.columns[feature_selector.get_support()],
    index = X_test.index)




# Cria tabela dos melhores indicadores selecionados
selector_scores = pd.DataFrame(zip(X_train.columns, feature_selector.scores_)).set_index(0)
indicators['Score'] = selector_scores

selected_indicators = indicators[indicators.index.isin(feature_selector.get_support())]


selected_indicators.to_csv(
    TABLES_PATH +'selecaoIndicadores.csv',
    columns = ['Indicator Name', 'Score'])



### APLICAÇÃO DOS MODELOS

random_forest = RandomForestRegressor(random_state=0)
random_forest.fit(X_train_selected, y_train)


y_pred = random_forest.predict(X_test_selected)
score = random_forest.score(X_test_selected, y_test)


### Criação do dataframe para análise sobre o resultado

results = y_test.reset_index()
results = results.join(countries[['Region']], on='Country Code')
results['Prediction'] = y_pred
results['Abs. Error'] = abs(results[gdp_growth_code] - results['Prediction'])


### Criação de gráficos para análise sobre o resultado
## Calcula a previsão sobre os dados de teste



# Cria um gráfico de disperção
plt.scatter(y_test, y_pred, alpha=0.5)
plt.axis('equal')
plt.plot([-50, 50], [-50, 50], color='r')
plt.xlabel('Valores Reais')
plt.ylabel('Valores Preditos')
plt.title('Valores Reais vs. Valores Preditos')
plt.grid(True)
plt.show()

## Calcula a diferença entre os valores reais x valores preditos (residuos)

residuals = abs(y_test - y_pred)

# Cria um gráfico de resíduos
plt.figure(figsize=(10, 6))
plt.scatter(y_pred, residuals, alpha=0.5)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Valores Preditos')
plt.ylabel('Resíduos')
plt.title('Gráfico de Resíduos')
plt.grid(True)
plt.show()