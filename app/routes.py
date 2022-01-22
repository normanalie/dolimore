from flask import render_template

from app import app


@app.route('/')
def index():
    return render_template('index.html')

@app.route('/contract')
def base():
    return render_template('contract.html')

@app.route('/mailing')
def mailing():
    return render_template('mailing.html')