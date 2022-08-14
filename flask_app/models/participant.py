from multiprocessing.forkserver import connect_to_new_process
from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

db ="collaborative_workout"

class Participant:
    def __init__(self , data ):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
    
    @classmethod
    def save(cls, data):
        query = "INSERT INTO participants (first_name, last_name, email, password, created_at, updated_at) VALUES (%(first_name)s,%(last_name)s,%(email)s,%(password)s,NOW(),NOW());"
        return connectToMySQL(db).query_db( query, data)
    @staticmethod
    def login_validation(data):
        valid = True
        query = "SELECT * FROM participants WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) >= 1:
            flash("Email already taken.")
            valid=False
        if not EMAIL_REGEX.match(data['email']):
            flash("Email must be formatted correctly")
            valid=False
        if len(data['first_name']) < 3:
            flash("First name must contain 3 characters")
            valid= False
        if len(data['last_name']) < 3:
            flash("Last name must contain 3 characters")
            valid= False
        if len(data['password']) < 8:
            flash("Password must contain 8 characters")
            valid= False
        if data['password'] != data['confirm']:
            flash("Passwords must match")
        return valid

    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM participants WHERE email = %(email)s;"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_by_id(cls,id):
        # query = "SELECT id, first_name, last_name, email,  FROM participants WHERE id = %(participant_id)s"
        query = """SELECT p.first_name, p.last_name, p.id, participant_id, SUM(w.points_earned) AS total_points 
                    FROM participants_has_workouts AS phw 
                    JOIN workouts AS w 
                    ON phw.workout_id = w.id
                    JOIN participants as p
                    ON phw.participant_id = p.id
                    WHERE participant_id = %(participant_id)s;"""
        return connectToMySQL(db).query_db(query, id)[0]