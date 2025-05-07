from flask import render_template, redirect, url_for
from shiftapp import app

@app.route('/')
def home():
    return redirect(url_for('login'))

@app.route('/login')
def login():
    return render_template('login.html')
