from flask import Flask, render_template, redirect, url_for, request

from kmeans import open_csv,results
#from TD_IDF import get_content_based_recommendations
from colab_filt import get_recommendations, data_music
from top_charts import get_popularity_recommendations

import pandas as pd
from scipy.sparse import csr_matrix
from implicit.als import AlternatingLeastSquares

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/methods')
def methods():
    return render_template('methods.html')

@app.route('/next_page', methods=['GET', 'POST'])
def next_page():
    num_input_songs = 0
    num_recommendations = 0

    if request.method == 'POST':
        if 'song_count' in request.form and 'rec_count' in request.form:
            num_input_songs = int(request.form['song_count'])
            num_recommendations = int(request.form['rec_count'])
        return render_template('next_page.html', num_input_songs=num_input_songs,num_recommendations=num_recommendations)
    return render_template('next_page.html')



@app.route('/enter_song/<int:num_input_songs>&<int:num_recommendations>',methods=['GET','POST'] )
def rec(num_input_songs,num_recommendations):
    input_songs = []
    if request.method == 'POST':
        for i in range(num_input_songs):
            song_name = request.form.get(f'song{i}')
            if song_name:
                input_songs.append(song_name)
            # input_songs.append(request.form[f'song{i}'])
        return render_template('next_page.html',num_input_songs=num_input_songs,input_songs=input_songs,num_recommendations=num_recommendations)
    return render_template('next_page.html')


@app.route('/result/<int:num_recommendations>&<path:input_songs>', methods=['GET','POST'])
def result( num_recommendations, input_songs):
    music_data = open_csv()
    input_songs_list = input_songs.split(',')  # Разделение строки на элементы массива по запятой
    recommended_songs = results(music_data,num_recommendations,input_songs_list)
    recommended_songs_list = recommended_songs.to_dict('records')

    return render_template('result.html',recommended_songs=recommended_songs_list)

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/manual')
def manual():
    return render_template('manual.html')

### Метод Колабортавної фільтрації
@app.route('/col_fil', methods=['GET', 'POST'])
def col_fil():
    if request.method == 'POST':
        song_name = request.form.get('song_name')
        return redirect(url_for('col_fil_result', song_name=song_name))
    return render_template('col_fil.html')

@app.route('/col_fil_result', methods=['GET', 'POST'])
def col_fil_result():
    if request.method == 'POST':
        song_name = request.form.get('song_name')
        recommendations = get_recommendations(song_name, num_recommendations=5)
        if recommendations:
            return render_template('col_fil_result.html', song_name=song_name, recommendations=recommendations)
        else:
            return render_template('col_fil_result.html', song_name=song_name, recommendations=[])
    else:
        return redirect(url_for('col_fil'))

@app.route('/top_charts')
def top_charts():
    num_recommendations = 10
    recommended_songs = get_popularity_recommendations(num_recommendations)
    return render_template('top_charts.html', recommended_songs=recommended_songs)





if __name__ == '__main__':
    app.run(debug=True)