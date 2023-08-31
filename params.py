""" Define parâmetros para a extração e tratamento do dataframe
"""

# Início do intervalo de anos do qual serão extraídos os dados
initial_year = 2008

# Final do intervalo de anos do qual serão extraídos os dados
final_year = 2017

# Porcentagem de valores não-nulos que os indicadores precisam ter ao longo do dataframe
# para não serem excluídos pelo filtro
thresh = 0.8

# Filtro de países que devem ser mantidos no dataframe
countries = [
    # América do Sul
    'Brazil',
    'Argentina',
    'Bolivia',
    'Chile',
    'Colombia',
    'Ecuador',
    'Guyana',
    'Paraguay',
    'Peru',
    'Suriname',
    'Uruguay',
    'Venezuela, RB',
    # América do Norte
    'Mexico',
    'United States',
    # Europa
    'France',
    'Germany',
    'Portugal',
    'Romania',
    'Russian Federation',
    'Spain',
    # África
    'Angola',
    'Congo, Dem. Rep.',
    'Egypt, Arab Rep.',
    'Nigeria',
    'South Africa',
    # Ásia
    'China',
    'India',
    'Indonesia',
    'Japan',
    'Korea, Rep.',
    'Saudi Arabia',
    # Oceania
    'Australia'
]
