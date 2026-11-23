import pandas as pd

df = pd.read_csv("data/postings_sample.csv", nrows=5000)
print(df.shape)
print(df.columns.tolist())
print(df.isna().sum())
print(df[["title", "location", "min_salary", "max_salary", "pay_period"]].head(10))