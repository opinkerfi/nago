#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" A http server written in flask. Allows two or more nago instances to talk with each other

"""
from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash

app = Flask(__name__)
app.secret_key = 'bla'


def login_required(func, permission=None):
    """ decorate with this function in order to require a valid token for any view

     If no token is present you will be sent to a login page
    """
    def decorated_view(*args, **kwargs):
        if not check_token():
            return login()
        return func(*args, **kwargs)
    return decorated_view

def check_token():
    if 'token' in request.args :
        session['token'] = request.args.get('token')
    elif request.method == 'POST' and 'token' in request.form:
        session['token'] = request.form.get('token')

    if session.get('token'):
        return True
    else:
        return False

@app.route('/', methods=['GET', 'POST'])
@login_required
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')


if __name__ == '__main__':
    app.run(debug=True)