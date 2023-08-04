from os import listdir
import pandas as pd

def merge_dataframes(initial_year: int, final_year: int):
    """
    Lê todos os arquivos presentes na pasta Data_extracts (exceto as de metadados)
    e os combina em um único dataframe.
    """
    dataframes = []
    for y in range(initial_year, final_year+1):
        year = str(y)
        # Obtém nome da pasta e do arquivo csv a ser lido
        folder = './Data_extracts/' + year
        [filename] = [file for file in listdir(folder) if file.endswith('_Data.csv')]

        # Cria dataframe a partir do arquivo
        data = pd.read_csv(
            folder+'/'+filename,
            usecols= lambda col: col!='Series Name', # Filtra colunas que não serão úteis no momento
            na_values='..'    # Interpreta '..' como NaN (valor nulo)
        )
        data = data[:-5]        # remove as 5 últimas linhas (metadados)
        data = data.rename(columns={f'{year} [YR{year}]' : year})
        data['Year'] = y

        # Transpõe os valores de 'Series Code' como novas colunas, chegando a 1481 colunas ao todo
        data = data.pivot(
            index=['Country Name', 'Country Code', 'Year'],
            columns='Series Code',
            values=year
        ).reset_index()
        # Após o pré-processamento, insere dataframe no array
        dataframes.append(data)
    # Ao final do loop, faz a concatenação de todos os dataframes do array
    return pd.concat(dataframes).sort_values(['Country Name', 'Year']).reset_index(drop=True)

df = merge_dataframes(2008,2022)