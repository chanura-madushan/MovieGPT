import pandas as pd
dataset_file = "data/netflix_titles.csv"


df=pd.read_csv(dataset_file)

    #rows and columns
print(df.shape)

    #first 5 movies
print(df.head())

    #last 5 movies
print(df.tail())

    #edata types present
print(df.dtypes)

    #column names
print(df.columns.tolist())

    #count of empty columns
print(df.isnull().sum())
