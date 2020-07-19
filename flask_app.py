
# A very simple Flask Hello World app for you to get started with...

from flask import Flask
import json

app = Flask(__name__)

@app.route('/')
def hello_world():
    return 'Test site is working!'

@app.route('/bot')
def process():
    return '';