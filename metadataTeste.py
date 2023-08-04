from os import listdir
import pandas as pd

def get_series_metadata():
    """
    Cria dicionário a partir da planilha de metadados dos indicadores socioeconômicos
    associando o nome de cada indicador à sua chave única - uma string menor
    """
    folder = './Data_extracts/Metadata_series'
    [filename] = [file for file in listdir(folder) if file.endswith('.xlsx')]
    return dict(
        pd.read_excel(folder+'/'+filename, usecols=['Code','Indicator Name'])
        .values)
