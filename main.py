from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from flask_sqlalchemy import SQLAlchemy
import requests
from timedata import Schedules

app = Flask(__name__)
app.config['SECRET_KEY'] = 'mysecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/news', methods=['GET', 'POST'])
def news():
    access_token = 'ecaef858ecaef858ecaef858b3efb86890eecaeecaef85889dc84fdd39a62ad2612e4bf'
    group_id = '213320340'
    count = 15  # Количество постов, которые вы хотите получить

    url = f'https://api.vk.com/method/wall.get?owner_id=-{group_id}&count={count}&access_token={access_token}&v=5.131'
    response = requests.get(url)
    data = response.json()

    posts = data['response']['items']
    for post in posts:
        attachments = post.get('attachments', [])

        for attachment in attachments:
            if attachment['type'] == 'photo':
                # Получаем URL изображения
                photo_url = attachment['photo']['sizes'][-1]['url']

                # Добавляем URL изображения к посту
                post.setdefault('photos', []).append(photo_url)

    return render_template('news.html', posts=posts)

@app.route('/timedata')
def timedata():
    schedules=Schedules()
    return render_template('timedata.html', schedules=schedules)


if __name__ == '__main__':
    app.run(debug=True, port=5005)