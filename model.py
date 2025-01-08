""" Passo 3: realiza a modelagem com Scikit-Learn a partir da base de dados tratada nos passos anteriores.
"""
import pandas as pd
import matplotlib.pyplot as plt

from sklearn.feature_selection import SelectKBest, r_regression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import KNNImputer

### Parâmetros

DATAFRAMES_PATH = './dataframes/'
TABLES_PATH = './material_overleaf/tabelas/'

TRANSFORMED_DF_PATH = DATAFRAMES_PATH + 'WDItransformada.csv'
MAIN_DF_PATH = DATAFRAMES_PATH + 'WDIPreProcessada.csv'
RAW_DF_PATH = DATAFRAMES_PATH + 'WDICSV.csv'
COUNTRIES_PATH = DATAFRAMES_PATH + 'WDICountry.csv'
INDICATORS_PATH = DATAFRAMES_PATH + 'WDISeries.csv'

YEARS_TO_DROP = 16                  # 1/4 do total de anos
COUNTRIES_TO_DROP = 28              # aprox. 10% dos 266 países e regiões
INDICATORS_NOT_NAN_THRESHOLD = 0.6  # exclui todo indicador com + de 40% valores nulos
KNN_IMPUTER_NEIGHBOURS = 10
TEST_SET_RATIO = 0.25
FEATURES_TO_SELECT = 32


### Extração dos dados

wdi = pd.read_csv(MAIN_DF_PATH)
preprocessed_wdi = pd.read_csv(TRANSFORMED_DF_PATH)
raw_wdi = pd.read_csv(RAW_DF_PATH)
countries = pd.read_csv(COUNTRIES_PATH, index_col='Country Code')
indicators = pd.read_csv(INDICATORS_PATH, index_col='Series Code')


### Processamento dos conjuntos de teste e treinamento

# Separa as variáveis de entrada (X) e variável alvo (y)
[gdp_growth_code] = indicators.query("`Indicator Name` == 'GDP growth (annual %)'").index
wdi = wdi.set_index(['Country Name', 'Country Code', 'Year'])
X = wdi.drop(columns=[gdp_growth_code])
y = wdi[gdp_growth_code]

# Normaliza o conjunto de entrada
# scaler = StandardScaler()
# X_scaled = scaler.fit_transform(X, y)

# Preenche os valores vazios no conjunto de entrada

imputer = KNNImputer(n_neighbors=KNN_IMPUTER_NEIGHBOURS, weights='uniform')
X_imputed = imputer.fit_transform(X)
X_imputed = pd.DataFrame(X_imputed, columns=X.columns, index=X.index)



# Separa em conjuntos de teste e treinamento
X_train, X_test, y_train, y_test = train_test_split(
    X_imputed, y, test_size=TEST_SET_RATIO, random_state=0)

# Filtra os melhores indicadores, conforme parâmetro
feature_selector = SelectKBest(r_regression, k=FEATURES_TO_SELECT)
feature_selector.fit(X_train, y_train)
X_train_selected = pd.DataFrame(
    feature_selector.transform(X_train),
    columns = X_train.columns[feature_selector.get_support()],
    index = X_train.index
)
X_test_selected = pd.DataFrame(
    feature_selector.transform(X_test),
    columns = X_test.columns[feature_selector.get_support()],
    index = X_test.index
)

# Cria tabela dos melhores indicadores selecionados
selected_indicators = indicators[indicators.index.isin(X_train_selected.columns)]
selected_indicators.to_csv(
    TABLES_PATH +'selecaoIndicadores.csv',
    columns = ['Indicator Name']
)



### Aplicação dos modelos

random_forest = RandomForestRegressor(random_state=0)
random_forest.fit(X_train_selected, y_train)

score = random_forest.score(X_test_selected, y_test)



### Criação de gráficos para análise sobre o resultado
## Calcula a previsão sobre os dados de teste

y_pred = random_forest.predict(X_test_selected)

# Cria um gráfico de disperção
plt.scatter(y_test, y_pred, alpha=0.5)
plt.xlabel('Valores Reais')
plt.ylabel('Valores Preditos')
plt.title('Valores Reais vs. Valores Preditos')
plt.show()

## Calcula a diferença entre os valores reais x valores preditos (residuos)

residuals = y_test - y_pred

# Cria um gráfico de resíduos
plt.figure(figsize=(10, 6))
plt.scatter(y_pred, residuals, alpha=0.5)
plt.axhline(y=0, color='r', linestyle='--')
plt.xlabel('Valores Preditos')
plt.ylabel('Resíduos')
plt.title('Gráfico de Resíduos')
plt.grid(True)
plt.show()