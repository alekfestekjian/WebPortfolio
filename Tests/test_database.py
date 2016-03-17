import sys
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from contextlib import closing
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
import parser_test
import test_app
app = Flask(__name__)

"""
Adding a comment to database and checking that it exits
"""
def test_commenting():
    with app.app_context():
        test_comment = "my test comment"
        test_title = "test username"
        test_file = "testing.py"
        db = test_app.get_db()
        db.execute('insert into entries (title, text,file) values (?, ?, ?)',
            [test_title, test_comment,test_file])
        db.commit()

        test_db = db.execute('select * from entries')
        test_entry = test_db.fetchall()
        for test in test_entry:
            assert test[1] == test_title
            assert test[2] == test_comment
            assert test[3] == test_file
        db.execute('delete from entries where file=?',(test_file,))
        db.commit()


"""
Adding a reply to database and checking that it exits
"""
def test_replying():
    with app.app_context():
        test_parent  = "3"
        test_comment = "my reply comment"
        test_title = "reply username"
        test_file = "reply.py"
        db = test_app.get_db()
        db.execute('insert into reply_entries (parent_id,title, text,file) values (?, ?, ?,?)',
            [test_parent, test_title,test_comment,test_file])
        db.commit()

        test_db = db.execute('select * from reply_entries')
        test_entry = test_db.fetchall()
        for test in test_entry:
            assert test[1] == test_parent
            assert test[2] == test_title
            assert test[3] == test_comment
            assert test[4] == test_file

        db.execute('delete from reply_entries where file=?',(test_file,))
        db.commit()
"""
Adding a naughty word  to database and checking that it becomes filtered
"""
def test_naughty_words():
    with app.app_context():
        test_comment = "shit poop"
        test_title = "shit poop"
        test_file = "test.py"
        db = test_app.get_db()
        new_title,new_comment = test_app.filter(test_title,test_comment)
        db.execute('insert into entries (title, text,file) values (?, ?, ?)',
            [new_title, new_comment,test_file])
        db.commit()

        test_db = db.execute('select * from entries')
        test_entry = test_db.fetchall()
        for test in test_entry:
            assert test[1] != test_title
            assert test[2] != test_comment
        db.execute('delete from entries where file=?',(test_file,))
        db.commit()
