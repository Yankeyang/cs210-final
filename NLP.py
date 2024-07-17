import pandas as pd
import spacy
nlp = spacy.load("en_core_web_md")
url = 'https://raw.githubusercontent.com/Yankeyang/cs210-final/main/games.csv'
games = pd.read_csv(url)

games['Release Date'] = pd.to_datetime(games['Release Date'], errors='coerce')
games['Year'] = games['Release Date'].dt.year

def conv_rev(rev):
    if isinstance(rev, str):
        rev = rev.lower().replace(' ', '')
        if 'k' in rev:
            return float(rev.replace('k', '')) * 1000 + 1
    try:
        return float(rev)
    except ValueError:
        return 0

games['Reviews'] = games['Number of Reviews'].apply(conv_rev)

filtered = games[(games['Year'] >= 2010) & (games['Year'] <= 2022)]

topgames = filtered.loc[filtered.groupby('Year')['Reviews'].idxmax()]
topgames = topgames.sort_values('Year')
summ = topgames[['Year', 'Title', 'Summary', 'Reviews']].copy()
trendingurl = 'https://raw.githubusercontent.com/Yankeyang/cs210-final/main/trendingwords.csv'
trendingdf = pd.read_csv(trendingurl)
trendwords = trendingdf.set_index('Year')['Words'].to_dict()

def calculate_overlap(summary, year):
    summarydoc = nlp(summary)
    overlapinfo = []
    for yr, words in trendwords.items():
        words_doc = nlp(words)
        similarity = summarydoc.similarity(words_doc)
        overlapinfo.append((similarity, abs(year - yr)))
    return overlapinfo

summ['OverlapInfo'] = summ.apply(lambda row: calculate_overlap(row['Summary'], row['Year']), axis=1)

summ[['Year', 'Title', 'Summary', 'OverlapInfo']].to_csv('gameswithoverlap.csv', index=False)

print("gameswithoverlap.csv")
