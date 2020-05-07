import pandas as pd
import glob

columns = ["Date", "Username","To","Replies",
            "Retweets","Favorites","Text","Geo",
           "Mentions","Hashtags","Id","Permalink"]
df = pd.DataFrame([], columns = columns) 
for name in glob.glob('data/corona virus/*.csv'): 
    df_temp = pd.read_csv(name)
    df = df.append(df_temp.drop(['Unnamed: 0'], axis=1))
for name in glob.glob('data/coronavirus/*.csv'): 
    df_temp = pd.read_csv(name)
    df = df.append(df_temp.drop(['Unnamed: 0'], axis=1))
for name in glob.glob('data/Covid-19/*.csv'): 
    df_temp = pd.read_csv(name)
    df = df.append(df_temp.drop(['Unnamed: 0'], axis=1))

df['Date'] = pd.to_datetime(df['Date'], format="%Y-%m-%d %H:%M:%S")
df = df.sort_values(by=["Date"])
df = df.reset_index(drop=True)

df_print = df[["Date","Text"]]
df_print["Date"] = df_print["Date"].dt.date
df_print.drop_duplicates(inplace=True) 
df_print = df_print.reset_index(drop=True)

df_print.to_csv("data.csv")