#!/usr/bin/env python
# -*- coding: utf-8 -*-
""" A http server written in flask. Allows two or more nago instances to talk with each other

"""
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Hello World!'

if __name__ == '__main__':
    app.run(debug=True)