import pandas as pd
import re 

def tweet_cleaner(text):
    # remove mention
    text = re.sub(r'@[A-Za-z0-9]+', '', text)
    # remove website
    text = re.sub(r'https?://[A-Za-z0-9./]+', '',text)
    # remove non-ASCII
    text = re.sub(r'[^\x00-\x7F]+',' ', text)
    # remove keywords
    text = re.sub(r'corona ?virus', '',text)
    text = re.sub(r'covid[\W|_]19', '',text)
    text = re.sub(r'covid', '',text)
    
    text = text[1:len(text)-1].split()
    newText = []
    for token in text:   
        # remove website
        if 'twitter' in token or 'com' in token:
            continue
        newText.append(token) 
    newText = ' '.join(newText)
    # keep the letter
    newText = re.sub("[^a-zA-Z]", " ", newText)
    newText  = newText.split()
    newText  = [i.strip() for i in newText]
    newText = ' '.join(newText)
    return str(newText)

df = pd.read_csv("data.csv")
df = df.drop(['Unnamed: 0'], axis=1)
df['Text'] = df["Text"].apply(lambda x: tweet_cleaner(x.lower()))
df = df[df["Text"] != ""]
df = df.reset_index(drop=True)
df.to_csv("dataClean.csv")