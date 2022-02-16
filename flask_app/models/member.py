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
        return connectToMySQL('dojos_ninjas').query_db( query, data)
    @staticmethod
    def verify_member(member):
        is_valid = True
        if len(member['firstname'])< 2:
            is_valid = False
            flash('Name must be more than 2 characters')
        elif len(member['lastname'])< 2:
            is_valid = False
            flash('Last Name must be more than 2 characters')
        elif not EMAIL_REGEX.match(member['email']): 
            flash("Invalid email address!")
            is_valid = False
        elif member['password'] < 8:
            flash('Password must be 8 at least characters long ')
            is_valid = False
        return is_valid