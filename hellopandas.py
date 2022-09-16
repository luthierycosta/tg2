import pandas as pd

tabela = pd.read_csv("Data.csv")

print(tabela.head(20))
print(tabela.info())