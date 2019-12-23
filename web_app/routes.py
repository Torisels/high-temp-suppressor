from flask import render_template, url_for, flash, redirect, request, abort
from web_app import app


@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')
