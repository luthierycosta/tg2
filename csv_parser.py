""" Módulo com as funções para extrair e lidar com os arquivos do repositório,
onde estão contidos os dados a serem minerados.
"""
from os import listdir
import pandas as pd

DATA_PATH = './Data_extracts/'

def get_dataframes(initial_year: int, final_year: int):
    """
    Lê todos os arquivos presentes na pasta Data_extracts (exceto as de metadados)
    e os combina em um único dataframe.
    """
    dataframes = []
    # Loop para inserir os dataframes de cada ano (ou cada arquivo) em um array
    for y in range(initial_year, final_year+1):
        year = str(y)

        folder = DATA_PATH + year
        [filename] = [file for file in listdir(folder) if file.endswith('_Data.csv')]

        data = pd.read_csv(
            folder+'/'+filename,
            usecols= lambda col: col!='Series Name',
            na_values='..'
        )
        # remove as 5 últimas linhas (metadados) e manipula os dados de 'Year'
        data = data[:-5]
        data = data.rename(columns={f'{year} [YR{year}]' : year})
        data['Year'] = y

        # Transpõe os indicadores (Series) como colunas em vez de linhas
        data = data.pivot(
            index=['Country Name', 'Country Code', 'Year'],
            columns='Series Code',
            values=year
        ).reset_index()

        dataframes.append(data)

    # Por fim, retorna a concatenação de toda a lista de dataframes em um só
    return pd.concat(dataframes).sort_values(['Country Name', 'Year']).reset_index(drop=True)


def get_metadata(folder_: str):
    """
    Cria um dataframe a partir da planilha de metadados contida na pasta informada 
    """
    folder = DATA_PATH + folder_
    [filename] = [file for file in listdir(folder) if file.endswith('.xlsx')]
    return pd.read_excel(folder+'/'+filename, index_col='Code')
