import pandas as pd

url = 'https://raw.githubusercontent.com/Yankeyang/cs210-final/main/games.csv'
games_data = pd.read_csv(url)

games_data['Release Date'] = pd.to_datetime(games_data['Release Date'], errors='coerce')
games_data['Year'] = games_data['Release Date'].dt.year

def convert_reviews(reviews):
    if isinstance(reviews, str):
        reviews = reviews.lower().replace(' ', '')
        if 'k' in reviews:
            return float(reviews.replace('k', '')) * 1000 + 1  # 确保带k的值更大
    try:
        return float(reviews)
    except ValueError:
        return 0

games_data['Number of Reviews'] = games_data['Number of Reviews'].apply(convert_reviews)

filtered_data = games_data[(games_data['Year'] >= 2010) & (games_data['Year'] <= 2022)]

max_reviews_per_year = filtered_data.loc[filtered_data.groupby('Year')['Number of Reviews'].idxmax()]

max_reviews_per_year = max_reviews_per_year.sort_values('Year')

print(max_reviews_per_year[['Year', 'Title', 'Number of Reviews']])
summaries = max_reviews_per_year[['Year', 'Title', 'Summary']]

print(summaries)
