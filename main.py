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
    count = 15

    url = f'https://api.vk.com/method/wall.get?owner_id=-{group_id}&count={count}&access_token={access_token}&v=5.131'
    response = requests.get(url)
    data = response.json()

    if 'response' not in data:
        return "Error fetching data from VK API", 500

    posts = data['response']['items']
    for post in posts:
        attachments = post.get('attachments', [])
        photos = []
        videos = []

        for attachment in attachments:
            if attachment['type'] == 'photo':
                photo_url = attachment['photo']['sizes'][-1]['url']
                photos.append(photo_url)
            elif attachment['type'] == 'video':
                video_id = attachment['video']['id']
                owner_id = attachment['video']['owner_id']
                access_key = attachment['video'].get('access_key', '')
                video_url = f'https://vk.com/video{owner_id}_{video_id}' + (f'_{access_key}' if access_key else '')
                videos.append(video_url)

        post['photos'] = photos
        post['videos'] = videos

    return render_template('news.html', posts=posts)


@app.route('/timedata')
def timedata():
    schedules=Schedules()
    return render_template('timedata.html', schedules=schedules)


if __name__ == '__main__':
    app.run(debug=True, port=5005)