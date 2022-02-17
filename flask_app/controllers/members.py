from flask_app import app
from flask import render_template, redirect, request, session,flash
from flask_app.models.member import Members
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create_member', methods = ['POST'])
def create():
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    pw_hash2 = bcrypt.generate_password_hash(request.form['password2'])
    data = {
        'firstname' : request.form['firstname'],
        'lastname' : request.form['lastname'],
        'email' : request.form['email'],
        'password': pw_hash
    }
    if pw_hash != pw_hash2:
        flash('Both passwords muct match')
        return redirect('/')
    friends = Members.get_by_email(data)
    print(friends)
    if not Members.verify_member(request.form):
        return redirect('/')
    friends = Members.save(data)
    return redirect('/')
@app.route('/login', methods=['POST'])
def login():
    data = { "email" : request.form["email"] }
    user_in_db = Members.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_id'] = user_in_db.id
    session['user_name'] = user_in_db.firstname
    session['logged_in'] = True
    if session['logged_in'] == True:
        return render_template("home.html", name = session['user_name'])
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect('/')