from os import listdir
import pandas as pd

# Cria array que armazenará os dataframes ano a ano
dataframes = []

for y in range(2008, 2022+1):

    year = str(y)
    # Obtém nome da pasta e do arquivo csv a ser lido
    folder = './Data_extracts/' + year
    [filename] = [file for file in listdir(folder) if file.endswith('_Data.csv')]

    # Cria dataframe a partir do arquivo
    df = pd.read_csv(
        folder+'/'+filename,
        usecols = lambda col: col != 'Series Name', # Filtra colunas que não serão úteis no momento
        na_values = '..'    # Interpreta '..' como NaN (valor nulo)
    )

    df = df[:-5]        # remove as 5 últimas linhas (metadados)
    df = df.rename(columns={f'{year} [YR{year}]' : year})
    df['Year'] = y

    # Transpõe os valores de 'Series Code' como novas colunas, chegando a 1481 colunas ao todo
    df = df.pivot(
        index=['Country Name', 'Country Code', 'Year'],
        columns='Series Code',
        values=year
    ).reset_index()
    # Após o pré-processamento, insere dataframe no array
    dataframes.append(df)

# Ao final do loop, faz a concatenação de todos os dataframes do array
finalData = pd.concat(dataframes).sort_values(['Country Name', 'Year']).reset_index(drop=True)
