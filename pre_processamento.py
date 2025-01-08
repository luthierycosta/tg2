""" Passo 2: usa o framework Pandas para o pré-processamento dos dados.
"""
import pandas as pd

### Constantes de ambiente

DATAFRAMES_PATH = './dataframes/'
TABLES_PATH = './material_overleaf/tabelas/'

TRANSFORMED_DF_PATH = DATAFRAMES_PATH + 'WDItransformada.csv'
MAIN_DF_PATH = DATAFRAMES_PATH + 'WDIPreProcessada.csv'
RAW_DF_PATH = DATAFRAMES_PATH + 'WDICSV.csv'
COUNTRIES_PATH = DATAFRAMES_PATH + 'WDICountry.csv'
INDICATORS_PATH = DATAFRAMES_PATH + 'WDISeries.csv'
INDICATORS_FULLINFO_PATH = TABLES_PATH + 'indicadoresfull.csv'


### Parâmetros

YEARS_TO_DROP = 16                  # 1/4 do total de anos
COUNTRIES_TO_DROP = 28              # aprox. 10% dos 266 países e regiões
INDICATORS_NOT_NAN_THRESHOLD = 0.6  # exclui todo indicador com + de 40% valores nulos


### Extração dos dados

wdi = pd.read_csv(TRANSFORMED_DF_PATH)
raw_wdi = pd.read_csv(RAW_DF_PATH)
countries = pd.read_csv(COUNTRIES_PATH, index_col='Country Code')
indicators = pd.read_csv(INDICATORS_PATH, index_col='Series Code')

# Cria tabela de todos os indicadores
indicators['Indicator Name'] = indicators['Indicator Name'].map(lambda x: x if len(x) <= 49 else x[:49] + '...')
indicators.sort_values(['Topic']).to_csv(
    TABLES_PATH + 'indicadoresfull.csv',
    columns = ['Indicator Name']
)


### Variáveis para análise sobre o dataset inicial

total_indicators = len(wdi.columns) - 3
total_countries = len(wdi.groupby('Country Code'))
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
    ylabel='Frequência de indicadores',
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
wdi = wdi.dropna(axis=1, thresh=INDICATORS_NOT_NAN_THRESHOLD*len(wdi))

# Cria tabela dos indicadores que passaram no filtro acima (apêndice D)
filtered_indicators = indicators[indicators.index.isin(wdi.columns)]
filtered_indicators.sort_values(['Series Code']).to_csv(
    TABLES_PATH + 'indicadoresFiltro.csv',
    columns = ['Indicator Name']
)

wdi.to_csv(MAIN_DF_PATH, index=False)