from flask_app import app
from flask import render_template, redirect, request, session,flash
from flask_app.models.member import Members
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

#STARTER TEMPLATE
@app.route('/')
def index():
    return render_template('index.html')

#CREATE USER CHECK FOR PASSWORD VALIDATION
@app.route('/create_member', methods = ['POST'])
def create():
    #HASHING INPUT PASSWORDS 1 AND 2 AND ASSIGNING THEM TO VARIABLES
    pw_hash = bcrypt.generate_password_hash(request.form['password'])
    print(pw_hash)
    pw_hash2 = bcrypt.generate_password_hash(request.form['password2'])
    print(pw_hash2)

    #CREATING DICTIONARY OF DATA FROM INPUT
    data = {
        'firstname' : request.form['firstname'],
        'lastname' : request.form['lastname'],
        'email' : request.form['email'],
        'password': pw_hash
    }
    #CHECKING IF PASSWORDS MATCH
    #if pw_hash != pw_hash2:
        #flash('Both passwords muct match')
        #return redirect('/')
    #GETTING THE USER WHO'S EMAIL MATCHES THAT OF GIVEN FORM
    x = {'email':request.form['email']}
    print(x)
    #CHECKING TO SEE IF ENTERED FORM MATERIAL PASSES VERIFICATION
    if not Members.verify_member(request.form):
        return redirect('/')
    # SAVING NEW MEMBER IN DATABASE
    else:    
        friends = Members.save(data)
        session['new'] = x
        return redirect('/creator')
#LOGING INTO ACCOUNT
@app.route('/login', methods=['POST'])
def login():
    #EMAIL TO BE CHECkED IN DATA BASE
    data = { "email" : request.form["email"] }
    user_in_db = Members.get_by_email(data)
    if not user_in_db:
        flash("Invalid Email/Password")
        return redirect("/")
    #CHECKING TO SEE IF PASSWORD MATCHES THE ONE IN THE DATABASE
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("Invalid Email/Password")
        return redirect('/')
    #CREATING SESSION INFO FOR USER'S LOGIN
    session['user_id'] = user_in_db.id
    session['user_name'] = user_in_db.firstname
    session['logged_in'] = True
    if session['logged_in'] == True:
        return render_template("home.html", name = session['user_name'])
@app.route('/logout')
def logout():
    session['logged_in'] = False
    return redirect('/')
@app.route('/creator')
def got_in():
    if 'new' in session:
        friends = session['new']
        x = Members.get_by_email(friends)
        session['user_id'] = x.id
        session['firstname'] = x.firstname
        session['logged_in'] = True
        if session['logged_in'] ==  True:
            return render_template('home.html' , name = session['firstname'])

