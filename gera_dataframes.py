""" Módulo com as funções para extrair
a base de dados de sua pasta original.
"""
import pandas as pd

EXTRACTS_PATH = '../Data/WDI_CSV_2024_06_28/'
WORKSPACE_PATH = './dataframes/'
RAW_FILENAME = 'WDICSV.csv'
COUNTRIES_FILENAME = 'WDICountry.csv'
SERIES_FILENAME = 'WDISeries.csv'
MAIN_FILENAME = 'WDItratado.csv'

def get_wdi_dataframe():
    """
    Lê os dados extraídos em csv e o transforma em um dataframe Pandas,
    além de realizar o tratamento com melt+pivot para
    mover os anos para representação em linhas
    e os atributos (indicadores) para representação em colunas.
    """
    return pd \
        .read_csv(
            EXTRACTS_PATH + RAW_FILENAME,
            usecols= lambda col: col!='Indicator Name'
            ) \
        .melt(
            id_vars=['Country Name', 'Country Code', 'Indicator Code'],
            var_name='Year',
            value_name = 'Value'
            ) \
        .pivot(
            index=['Country Name', 'Country Code', 'Year'],
            columns='Indicator Code',
            values='Value'
            ) \
        .reset_index()


data = get_wdi_dataframe()
data.to_csv(WORKSPACE_PATH + MAIN_FILENAME, index=False)
