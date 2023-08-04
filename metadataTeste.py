import os
import pandas as pd
import numpy as np


folder = './Data_extracts/Metadata_series'
[filename] = [file for file in os.listdir(folder) if file.endswith('.xlsx')]
mydict = dict(
    pd.read_excel(folder+'/'+filename, usecols=['Code','Indicator Name'])
    .values)

