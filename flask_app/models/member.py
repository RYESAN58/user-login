from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
class Members:
    def __init__(self, data):
        self.id = data['id']
        self.firstname = data['firstname']
        self.lastname = data['lastname']
        self.email = data['email']
        self.password = data['password']
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO accounts.members (firstname, lastname, email, password) VALUES (%(firstname)s, %(lastname)s, %(email)s, %(password)s);"
        return connectToMySQL('accounts').query_db( query, data)
    @staticmethod
    def verify_member(member):
        is_valid = True
        if len(member['firstname'])< 2:
            flash('Name must be more than 2 characters', "register")
            is_valid = False
        if len(member['lastname'])< 2:
            flash('Last Name must be more than 2 characters', "register")
            is_valid = False
        if not EMAIL_REGEX.match(member['email']): 
            flash("Invalid email address!")
            is_valid = False
        if len(member['password']) < 8:
            flash('Password must be 8 at least characters long ', "register")
            is_valid = False
        return is_valid
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM members WHERE email = %(email)s;"
        result = connectToMySQL("accounts").query_db(query,data)
        if len(result) < 1:
            return False
        return cls(result[0])
    @classmethod
    def verify_email(cls,data):
        is_valid = True
        query = 'SELECT * FROM members WHERE email = %(email)s;'
        result = connectToMySQL("accounts").query_db(query,data)
        print('THIS IS THE RESULTS',result)
        if len(result)  != 0:
            flash('This Email is already Taken', 'login')
            is_valid = False
        return is_valid