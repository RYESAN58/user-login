from flask_app import app
from flask import render_template, redirect, request, session,flash
from flask_app.models.member import Members

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_member', methods = ['POST'])
def create():
    data = {
        'firstname' : request.form['firstname'],
        'lastname' : request.form['lastname'],
        'email' : request.form['email'],
        'password': request.form['password']
    }
    if not Members.verify_member(request.form):
        return redirect('/')
    friends = Members.save(data)
    return redirect('/')