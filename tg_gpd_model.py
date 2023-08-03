import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import SelectKBest, mutual_info_regression
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor

wb2021 = pd.read_csv("../world_bank_dev_indicators_6_series_2021/world_bank_6_series_2021_data.csv")
#wb2020 = pd.read_csv("../world_bank_dev_indicators_2020/world_bank_2020_data.csv")
#wb2019 = pd.read_csv("../world_bank_dev_indicators_2019/world_bank_2019_data.csv")

# Create generic dataframe
df = wb2021

# Preprocess the data
df.rename(columns = {'GDP growth (annual %) [NY.GDP.MKTP.KD.ZG]':'gpd_growth_annual'}, inplace = True)
df.rename(columns = {'Unemployment, total (% of total labor force) (modeled ILO estimate) [SL.UEM.TOTL.ZS]':'unemployment_total'}, inplace = True)
df.rename(columns = {'Inflation, GDP deflator (annual %) [NY.GDP.DEFL.KD.ZG]':'inflation_gpd'}, inplace = True)
df.rename(columns = {'Expenditure on primary education (% of government expenditure on education) [SE.XPD.PRIM.ZS]':'expenditure_pe'}, inplace = True)

df = df.replace('..', '0.0')
df = df.dropna()  # Remove rows with only NaN values
df['gpd_growth_annual'] = df['gpd_growth_annual'].astype(float)  # Convert data string to float


X = df[['unemployment_total', 'inflation_gpd', 'expenditure_pe']]
y = df['gpd_growth_annual']

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# Select the top 3 most informative features using mutual information
feature_selector = SelectKBest(mutual_info_regression, k=3)
X_selected = feature_selector.fit_transform(X_scaled, y)

# Split the data into training and test sets
X_train, X_test, y_train, y_test = train_test_split(X_selected, y, test_size=0.2)

# Train a Random Forest Regressor model on the training data
model = RandomForestRegressor()
model.fit(X_train, y_train)

result = model.score(X_test, y_test)
print (f'result: {score:.2f}')