import pandas as pd
from sklearn.ensemble import HistGradientBoostingRegressor

df = pd.read_csv('./dataframe_series_code.csv')

# Tratar valores ausentes (NaN)
df.fillna(df.mean(numeric_only=True), inplace=True)

# Separar dados de treinamento e teste
train_data = df[df['Year'] != 2022]
test_data = df[df['Year'] == 2022]
columns = [col for col in df.columns if col not in ['Country Name', 'Year', 'NY.GDP.MKTP.KD.ZG']]

# Separar variáveis de entrada e valor alvo (GPD anual)
X_train = train_data[columns]
y_train = train_data[ 'NY.GDP.MKTP.KD.ZG']
X_test = test_data[columns]

# Criar e treinar o modelo
model = HistGradientBoostingRegressor()
model.fit(X_train, y_train)

# Fazer previsões para o ano de 2020
predictions = model.predict(X_test)

# Adicionar as previsões ao dataframe original
test_data['GPD_Annual_Predicted'] = predictions

# Filtrar colunas pro dataframe final
columns_to_keep = ['Country Name', 'Year', 'NY.GDP.MKTP.KD.ZG', 'GPD_Annual_Predicted']
gpd_prediction = test_data[columns_to_keep]

# Salvar em um arquivo CSV
gpd_prediction.to_csv('predicted_GDP_2022_dataframe.csv', index=False)
