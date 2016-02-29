from flask import Flask, render_template
from flask.ext.script import Manager

app = Flask(__name__)
app.config['DEBUG'] = True

manager = Manager(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/videos/')
def videos():
    return render_template('videos.html')

if __name__ == '__main__':
    manager.run()
