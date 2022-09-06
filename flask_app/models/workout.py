from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

db ="collaborative_workout"

class Workout:
    def __init__(self , data ):
        self.id = data['id']
        self.description = data['description']
        self.photo_url = data['photo_url']
        self.points_earned = data['points_earned']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.challenge_id = data['challenge_id']

    @classmethod
    def save(cls,data):
        query = "INSERT INTO workouts (description, photo_url, points_earned, created_at, updated_at, challenge_id) VALUES(%(description)s, %(photo_url)s, %(points_earned)s, NOW(), NOW(), %(challenge_id)s)"
        return connectToMySQL(db).query_db(query, data)

    @classmethod
    def get_participants_in_challenge(cls, challenge_id):
        query = """SELECT * FROM participants AS p 
                    JOIN participants_has_challenges AS phc 
                    ON p.id = phc.participants_id 
                    WHERE challenges_id = %(challenge_id)s;"""
        results = connectToMySQL(db).query_db(query, {"challenge_id": challenge_id})

        participants = []

        for row in results:
            participants.append(row)

        return results

    @classmethod
    def save_workout(cls, form_data, photo_url):
        
        query_data ={}

        for item in form_data.items():
            query_data[item[0]]=item[1]
        query_data["photo_url"]=photo_url

        query = """INSERT INTO workouts (description, photo_url, points_earned, created_at, updated_at, challenge_id) 
                    VALUES(%(description)s, %(photo_url)s, %(points_earned)s, NOW(), NOW(), %(challenge_id)s);"""
        return connectToMySQL(db).query_db(query, query_data)

    @staticmethod
    def get_latest_workout():
        query = """SELECT MAX( id ) AS mx FROM workouts;"""
        return connectToMySQL(db).query_db(query)[0]["mx"]
        
    @classmethod
    def associate_participants_and_workouts(cls, participant_id, workout_id):
        print(participant_id)
        print(workout_id)
        query = """INSERT INTO participants_has_workouts (participant_id, workout_id) 
                    VALUES(%(participant_id)s,%(workout_id)s);"""
        return connectToMySQL(db).query_db(query, {"participant_id" : participant_id, "workout_id": workout_id})

    @classmethod
    def get_all_in_challenges(cls, challenge_id):
        query = """SELECT 
	                w.id AS workout_id, 
	                w.description, 
                    w.photo_url, 
                    w.points_earned, 
                    w.created_at, 
                    challenge_id, 
                    participant_id, 
                    p.first_name, 
                    p.last_name 
                FROM workouts AS w
                JOIN participants_has_workouts AS phw
                ON w.id = phw.workout_id
                JOIN participants AS p
                ON phw.participant_id = p.id
                WHERE challenge_id = %(challenge_id)s;"""

        results = connectToMySQL(db).query_db(query, {'challenge_id' : challenge_id})

        workouts = []

        for row in results:
            workouts.append(row)
        
        return results

    @classmethod
    def workout_validate(cls, data):
        valid = True
        if len(data['description']) < 5:
            flash("Description must be at least 5 characters")
            valid = False
        return valid