import pandas as pd
from sklearn.cluster import KMeans


def open_csv():
    data = pd.read_csv('data_music.csv')


    selected_features = ['artists', 'duration_ms', 'danceability', 'name', 'release_date', 'tempo', 'energy']
    music_data = data[selected_features]

    # Обробка пропущених значень (якщо необхідно)
    music_data = music_data.dropna()

    # Масштабування числових ознак (duration_ms, danceability, tempo, energy)
    music_data[['duration_ms', 'danceability', 'tempo', 'energy']] = \
        (music_data[['duration_ms', 'danceability', 'tempo', 'energy']] - music_data[
            ['duration_ms', 'danceability', 'tempo', 'energy']].mean()) / \
        music_data[['duration_ms', 'danceability', 'tempo', 'energy']].std()

    # Кількість кластерів
    num_clusters = 10

    # Застосування алгоритму K-Means
    kmeans = KMeans(n_clusters=num_clusters, random_state=42)
    kmeans.fit(music_data[['duration_ms', 'danceability', 'tempo', 'energy']])

    # Додавання міток кластерів у дані
    music_data['cluster'] = kmeans.labels_
    return music_data


def results(music_data,num_recommendations,input_songs):
    # Фільтрація даних за введеними піснями
    filtered_data = music_data[music_data['name'].isin(input_songs)]

    # Отримання унікальних міток кластерів для введених пісень
    user_clusters = filtered_data['cluster'].unique()

    # Створення порожнього DataFrame для рекомендацій
    recommended_songs = pd.DataFrame()

    # Вибір пісень із кластерів, у яких знаходяться введені пісні
    for cluster in user_clusters:
        cluster_songs = music_data[music_data['cluster'] == cluster].sample(num_recommendations)
        recommended_songs = pd.concat([recommended_songs, cluster_songs])

    return recommended_songs