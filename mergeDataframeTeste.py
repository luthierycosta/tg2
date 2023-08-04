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
    data = pd.read_csv(
        folder+'/'+filename,
        usecols = lambda col: col != 'Series Name',
        na_values = '..'
    )
    # Remove as 5 últimas linhas (metadados)
    data = data[:-5]
    # Renomeia a coluna do ano para facilitar a manipulação
    data = data.rename(columns={f'{year} [YR{year}]' : year})
    # Cria atributo Year para diferenciar os registros desse dataframe dos outros anos
    data['Year'] = y
    
    # Transpõe os valores de 'Series Code' como novas colunas, passando para 1481 colunas ao todo
    data = data.pivot(index=['Country Name', 'Country Code', 'Year'], columns='Series Code', values=year).reset_index()
    # Após o tratamento, insere dataframe no array
    dataframes.append(data)

# Ao final do loop, retorna a concatenação de todos os dataframes do array
finalData = pd.concat(dataframes).sort_values(['Country Name', 'Year']).reset_index(drop=True)
