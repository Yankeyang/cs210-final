import pandas as pd

url = 'https://raw.githubusercontent.com/Yankeyang/cs210-final/main/games.csv'
gamesdata = pd.read_csv(url)

gamesdata['Release Date'] = pd.to_datetime(gamesdata['Release Date'], errors='coerce')
gamesdata['Year'] = gamesdata['Release Date'].dt.year

def convert_reviews(reviews):
    if isinstance(reviews, str):
        reviews = reviews.lower().replace(' ', '')
        if 'k' in reviews:
            return float(reviews.replace('k', '')) * 1000 + 1
    try:
        return float(reviews)
    except ValueError:
        return 0

gamesdata['Number of Reviews'] = gamesdata['Number of Reviews'].apply(convert_reviews)

filtereddata = gamesdata[(gamesdata['Year'] >= 2010) & (gamesdata['Year'] <= 2022)]

max = filtereddata.loc[filtereddata.groupby('Year')['Number of Reviews'].idxmax()]
max = max.sort_values('Year')

summaries = max[['Year', 'Title', 'Summary']].copy()

trends_url = 'https://raw.githubusercontent.com/Yankeyang/cs210-final/main/trendingwords.csv'
trends = pd.read_csv(trends_url)

trendingWords = trends.set_index('Year')['Words'].to_dict()

def calculateOverlap(summary, gameYear):
    overlapInfo = []
    summaryWordsSet = set(summary.lower().split())
    for year, words in trendingWords.items():
        trendingWordsSet = set(words.split(','))
        overlap = summaryWordsSet & trendingWordsSet
        if overlap:
            overlapInfo.append((overlap, abs(gameYear - year)))
    return overlapInfo

summaries.loc[:, 'OverlapInfo'] = summaries.apply(lambda row: calculateOverlap(row['Summary'], row['Year']), axis=1)

summaries[['Year', 'Title', 'Summary', 'OverlapInfo']].to_csv('gameswithoverlapinfo.csv', index=False)

print("Overlap data saved to gameswithoverlapinfo.csv")
