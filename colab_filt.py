import pandas as pd
import random

data_music = pd.read_csv("data_music.csv", usecols=["artists", "duration_ms", "danceability", "name", "release_date"])
data_music = data_music.drop_duplicates(subset="name").reset_index(drop=True)
data_music['name'] = data_music['name'].str.strip()

class KNNBasic:
    def __init__(self, sim_options):
        self.sim_options = sim_options

    def fit(self, trainset):
        pass

    def predict(self, song_index1, song_index2):

        # Пример расчета предсказанной оценки (здесь используется случайное число)
        est = random.uniform(0, 1)

        # Создаем объект Prediction с реальными значениями предсказанной оценки
        prediction = Prediction(song_index2, 0, est, 0)

        return prediction

class Prediction:
    def __init__(self, iid, uid, est, details):
        self.iid = iid
        self.uid = uid
        self.est = est
        self.details = details

model = KNNBasic(sim_options={'user_based': False})

class DataMusic:
    def __init__(self, data_music):
        self.data = data_music

    def __len__(self):
        return len(self.data)

    def raw_ratings(self):
        return [(i, i, 0) for i in range(len(self.data))]

    def to_inner_iid(self, song_index):
        return song_index

    def to_raw_iid(self, song_index):
        return song_index

dataset = DataMusic(data_music)
trainset = dataset
model.fit(trainset)

def get_recommendations(song_name, num_recommendations):
    song_index = data_music[data_music['name'].str.lower() == song_name.lower()].index[0]
    predictions = []
    for i in range(len(data_music)):
        if i != song_index:
            prediction = model.predict(song_index, i)
            song_info = (data_music.iloc[i]['name'], data_music.iloc[i]['artists'])
            predictions.append((song_info, prediction.est))
    predictions.sort(key=lambda x: x[1], reverse=True)
    top_recommendations = [(song_info[0], ' '.join(song_info[1].split(', ')).replace('[', '').replace(']', '').replace("'", '')) for song_info, _ in predictions[:num_recommendations]]
    return top_recommendations
