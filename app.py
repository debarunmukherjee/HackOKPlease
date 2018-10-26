from flask import Flask, render_template, session, g, request, redirect, url_for
import pymongo, json
from pymongo import MongoClient

app = Flask('__name__')
connection = MongoClient()
db = connection['HackOkPlease']
app.config['SECRET_KEY']='youcantguessthis'
print('Mongo connection status ' + db)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    print('login')
    session.pop('user', None)
    user = db['users'].find_one({'username': request.form['username']})
    print(user)
    if user != None and user['password'] == request.form['password']:
        session['user'] = user
        return user['username']
    return redirect(url_for('index'))

@app.before_request
def before_request():
    g.user = None
    if 'user' in session:
        g.user = session['user']

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8000, debug = True)
