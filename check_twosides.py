import pandas as pd

df = pd.read_parquet("twosides.parquet")

print(df.columns)

print()

print(df.head(10))