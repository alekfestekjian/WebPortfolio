# from flask import Flask
# from flask import request,render_template
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import parser

# FOllowed
#https://github.com/mitsuhiko/flask/blob/master/examples/flaskr/flaskr.py
DATABASE = 'Data/flask.db'
DEBUG = True
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


#DATABASE CODE
def init_db():
    with closing(connect_db()) as db:
        with app.open_resource('Test_Data/schema.sql', mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()


def connect_db():
    rv = sqlite3.connect('TEST_DATABASE')
    rv.row_factory = sqlite3.Row
    return rv
    # return sqlite3.connect('DATABASE')

def get_db():
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db

@app.teardown_appcontext
def close_connection(exception):
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()

# ADD QUERY DATABASE

# ROUTING
# @app.route('/')
# def show_entries():
#     db = get_db()
#     cur = db.execute('select title, text from entries order by id desc')
#     entries = cur.fetchall()
#     return render_template('show_entries.html', entries=entries)

@app.route('/')
def landing():
    svn_list = parser.parse_svn()
    db = get_db()
    cur = db.execute('select title, text from entries order by id desc')
    entries = cur.fetchall()
    return render_template('index.html',svn_list=svn_list[0],svn_log=svn_list[1],entries=entries)

#
# @app.route('/add', methods=['GET','POST'])
# def add_entry(assignment,file):
#
#     db = get_db()
#     db.execute('insert into entries (title, text) values (?, ?)',
#                [request.form['title'], request.form['text']])
#     db.commit()
#     flash('New entry was successfully posted')
#     return redirect(url_for('iframe',path=file,directory=assignment))

@app.route('/add/<directory>/<path>', methods=['POST'])
def add_entry(directory,path):
    db = get_db()
    unique_file = directory + "-" + path
    if request.form['text'] == "":
        return redirect(url_for('iframe',path=path,directory=directory))
    if request.form['title'] == "":
        return redirect(url_for('iframe',path=path,directory=directory))

    if request.form['reply'] == "":
        title = request.form['title']
        text = request.form['text']
        title,text = filter(request.form['title'],request.form['text'])
        db.execute('insert into entries (title, text,file) values (?, ?, ?)',
               [title, text,unique_file])
        db.commit()
    else:
        title = request.form['title']
        text = request.form['text']
        reply = request.form['reply']
        title,text = filter(request.form['title'],request.form['text'])
        print('This is STUPID')
        db.execute('insert into reply_entries (parent_id,title, text,file) values (?, ?, ?,?)',
               [str(reply),title, text,unique_file])
        db.commit()
    return redirect(url_for('iframe',path=path,directory=directory))

# For when you click on a specific assignment
@app.route('/<files>')
def files(files):
    svn_list = parser.parse_svn()
    return render_template('details.html',svn_list=svn_list[0],svn_log=svn_list[1],assignment=files)

#showing an iframe of specifiecd file
@app.route('/<directory>/<path>')
def iframe(directory,path):
    svn_list = parser.parse_svn()
    db = get_db()
    # filter(request.form['title'],request.form['text'])

    db.commit()
    comment = db.execute('select title, text, file,id from entries order by id desc')
    replies = db.execute('select title,text,parent_id from reply_entries order by child_id desc')

    entries = comment.fetchall()
    replies = replies.fetchall()
    return render_template('show_entries.html',svn_list=svn_list[0],svn_log=svn_list[1],path=path,directory=directory,entries=entries,replies=replies)

def filter(title,text):
    db = get_db()
    cur = db.execute('select * from naughty_words')
    replace = cur.fetchall()
    for word in replace:
        if word[0] in title:
            title = title.replace(word[0],word[1])
        if word[0] in text:
            text = text.replace(word[0],word[1])
    return title,text


if __name__ == '__main__':
    app.run(debug=True)
