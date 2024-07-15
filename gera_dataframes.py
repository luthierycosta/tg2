""" Módulo com as funções para extrair e lidar com os arquivos do repositório,
onde estão contidos os dados a serem minerados.
"""
import pandas as pd

EXTRACTS_PATH = '../Data/WDI_CSV_2024_06_28/'
WORKSPACE_PATH = './dataframes_tratados/'
MAIN_FILENAME = 'WDICSV.csv'
COUNTRIES_FILENAME = 'WDICountry.csv'


def get_main_dataframe():
    """
    Lê os dados extraídos em csv e o transforma em um dataframe Pandas,
    além de realizar o tratamento com melt+pivot para
    mover os anos para representação em linhas
    e os atributos (indicadores) para representação em colunas.
    """

    return pd \
        .read_csv(
            EXTRACTS_PATH + MAIN_FILENAME,
            usecols= lambda col: col!='Indicator Name',
            na_values=''
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

"""
def get_metadata(folder_: str):
    folder = DATA_PATH + folder_
    [filename] = [file for file in listdir(folder) if file.endswith('.xlsx')]
    return pd.read_excel(folder+'/'+filename, index_col='Code')
"""
data = get_main_dataframe()
data.to_csv(WORKSPACE_PATH + 'WDItratado.csv', index=False)

