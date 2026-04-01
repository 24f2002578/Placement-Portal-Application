from main import app
from flask import render_template, request, session, flash, redirect
from controller.models import *


@app.route('/home')
def home():
    return render_template('home.html') 

@app.route('/about')
def about():
    return 'about page'