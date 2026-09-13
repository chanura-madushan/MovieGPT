import pandas as pd
dataset_file = "data/netflix_titles.csv"


df=pd.read_csv(dataset_file)

    #first 5 movies
print(df.head())

    #edata types present
print(df.dtypes())

    #column names
print(df.columns.tolist())
