import pandas as pd

url = 'https://raw.githubusercontent.com/Yankeyang/cs210-final/main/games.csv'
games = pd.read_csv(url)

games['Release Date'] = pd.to_datetime(games['Release Date'], errors='coerce')
games['Year'] = games['Release Date'].dt.year

def convertrev(rev):
    if isinstance(rev, str):
        rev = rev.lower().replace(' ', '')
        if 'k' in rev:
            return float(rev.replace('k', '')) * 1000 + 1
    try:
        return float(rev)
    except ValueError:
        return 0

games['Reviews'] = games['Number of Reviews'].apply(convertrev)

filtered = games[(games['Year'] >= 2010) & (games['Year'] <= 2022)]
max_reviews = filtered.loc[filtered.groupby('Year')['Reviews'].idxmax()]
max_reviews = max_reviews.sort_values('Year')

summaries = max_reviews[['Year', 'Title', 'Summary', 'Reviews']].copy()

trending_url = 'https://raw.githubusercontent.com/Yankeyang/cs210-final/main/trendingwords.csv'
trending_df = pd.read_csv(trending_url)

trending_dict = trending_df.set_index('Year')['Words'].to_dict()

def calcscore(summary, game_year, reviews):
    summary_set = set(summary.lower().split())
    score = 0
    for year, words in trending_dict.items():
        words_set = set(words.replace('(', '').replace(')', '').replace('#', '').split(','))
        overlap = summary_set & words_set
        for word in overlap:
            D = abs(game_year - year)
            score += 1 / (D + 1)
    return reviews / score if score != 0 else 0

summaries['Score'] = summaries.apply(lambda row: calcscore(row['Summary'], row['Year'], row['Reviews']), axis=1)
summaries[['Year', 'Title', 'Summary', 'Score']].to_csv('games_with_scores.csv', index=False)

print("Scores saved to games_with_scores.csv")
