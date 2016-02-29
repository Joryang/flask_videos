from flask import Flask, render_template, redirect, session, url_for
from flask.ext.script import Manager
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from flask.ext.bootstrap import Bootstrap
from flask_wtf.file import FileField, FileAllowed, FileRequired
from werkzeug import secure_filename
from flask.ext.sqlalchemy import SQLAlchemy
import time
import random
import os

basedir = os.path.abspath(os.path.dirname(__file__))

class VideosUploadForm(Form):
    video_name = FileField('Upload video')
    submit = SubmitField('Submit')

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'hard to guess'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///'+os.path.join(basedir,'data.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

bootstrap = Bootstrap(app)
manager = Manager(app)
db = SQLAlchemy(app)

class Videos(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    video_name = db.Column(db.String(128), unique=True)

    def __repr__(self):
	return '<Videos %r>' % self.video_name

@app.route('/', methods=['GET', 'POST'])
def index():
    form = VideosUploadForm()
    if form.validate_on_submit():
	video_name = secure_filename(form.video_name.data.filename)
	if video_name:
	    vname = 'flask'+str(int(time.time()*random.randint(1,100))) + video_name
	    vid = Videos(video_name=vname)
	    db.session.add(vid)
	form.video_name.data.save('/var/www/wsgi-scripts/flask_videos/static/'+vname)
	form.video_name.data = ''
	return redirect(url_for('index'))
    videos = Videos.query.all()
    return render_template('index.html', form=form, videos=videos)

@app.route('/videos/')
def videos():
    return render_template('videos.html')

@app.route('/photos/')
def photos():
    return render_template('photos.html')

if __name__ == '__main__':
    manager.run()
