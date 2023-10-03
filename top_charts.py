import pandas as pd

# Загрузка данных из CSV-файла
data = pd.read_csv('data_music.csv')


# Функция для получения рекомендаций на основе популярности
def get_popularity_recommendations(num_recommendations):
    # Сортировка данных по популярности
    sorted_data = data.sort_values(by='popularity', ascending=False)

    # Получение рекомендаций
    recommendations = sorted_data[['name', 'artists', 'id']].head(num_recommendations)
    recommendations['spotify_link'] = 'https://open.spotify.com/search/' + recommendations['id'].astype(str)

    # Возвращение рекомендаций в виде списка словарей
    return recommendations.to_dict('records')
