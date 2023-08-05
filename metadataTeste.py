from os import listdir
import pandas as pd

BASE_FOLDER = './Data_extracts'

def get_series_metadata():
    """
    Cria dicionário a partir da planilha de metadados dos indicadores socioeconômicos
    associando o nome de cada indicador à sua chave única - uma string menor
    """
    folder = BASE_FOLDER + '/Metadata_series'
    [filename] = [file for file in listdir(folder) if file.endswith('.xlsx')]
    return dict(
        pd.read_excel(folder+'/'+filename, usecols=['Code','Indicator Name'])
        .values)

def get_countries_metadata():
    folder = BASE_FOLDER + '/Metadata_countries'
    [filename] = [file for file in listdir(folder) if file.endswith('.xlsx')]
    return pd.read_excel(folder+'/'+filename, index_col='Code')