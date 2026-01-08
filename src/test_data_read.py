import pandas as pd

df = pd.read_excel('Data/sample_data.xlsx')
print(df.head())
print("Columns:", list(df.columns))
print("Rows:", len(df))