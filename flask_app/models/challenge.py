from flask_app.config.mysqlconnection import connectToMySQL
import re
from flask import flash

db = "collaborative_workout"

class Challenge:
    def __init__(self , data ):
        self.id = data['id']
        self.name = data['name']
        self.prize = data['prize']
        self.winner = data['winner']
        self.expiration = data['expiration']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def save_challenge(cls, data):
        query = "INSERT INTO challenges (name, prize, expiration, created_at, updated_at) VALUES (%(name)s,%(prize)s,%(expiration)s,NOW(),NOW());"
        return connectToMySQL(db).query_db(query,data)

    
    @classmethod
    def get_all(cls):
        query = "SELECT * FROM challenges;"
        return connectToMySQL(db).query_db(query)

    @classmethod
    def get_all_by_id(cls, data):
        data = {id: data}
        query = "SELECT * FROM challenges;"
        return connectToMySQL(db).query_db(query, data)[0]

    @classmethod
    def get_challenge_and_participant(cls):
        query = "SELECT c.id AS c_id,c.name,c.prize,c.winner,c.expiration,c.created_at AS c_created_at,c.updated_at AS c_updated_at,phc.participants_id,phc.challenges_id,p.id AS p_id,p.first_name,p.last_name,p.email,p.password,p.created_at AS p_created_at,p.updated_at AS p_updated_at FROM challenges AS c JOIN participants_has_challenges AS phc ON c.id = phc.challenges_id JOIN participants AS p ON p.id = phc.participants_id;"
        results = connectToMySQL(db).query_db(query)

        challenges = []

        for row in results:

            challenges.append( {
                "c_id" : row["c_id"],
                "name" : row["c_id"],
                "prize" : row["prize"],
                "winner" : row["winner"],
                "expiration" : row["expiration"],
                "c_created_at" : row["c_created_at"],
                "c_updated_at" : row["c_updated_at"],
                "participants_id" : row["participants_id"],
                "challenges_id" : row["challenges_id"],
                "p_id" : row["p_id"],
                "first_name" : row["first_name"],
                "last_name" : row["last_name"],
                "email" : row["email"],
                "password" : row["password"],
                "p_created_at" : row["p_created_at"],
                "p_updated_at" : row["p_updated_at"]
            })
            
        return challenges

    @classmethod
    def p_in_c(cls,data):
        query = ("INSERT INTO participants_has_challenges (participants_id, challenges_id) VALUES(%(participants_id)s,%(challenges_id)s);")
        return connectToMySQL(db).query_db(query, data)

    @staticmethod
    def participate_validation(data):
        valid = True
        query = "SELECT * FROM participants_has_challenges WHERE challenges_id = %(challenges_id)s AND participants_id = %(participants_id)s;"
        results = connectToMySQL(db).query_db(query,data)
        if len(results) >= 1:
            flash("Woah slow down there champ... you can only enroll in a challenge once")
            valid = False
        return valid
    
    @classmethod
    def get_leaderboard_table(cls, challenge_id):
        query = """SELECT p.first_name, p.last_name, p.id, participant_id, SUM(w.points_earned) AS total_points 
                    FROM participants_has_workouts AS phw 
                    JOIN workouts AS w 
                    ON phw.workout_id = w.id
                    JOIN participants as p
                    ON phw.participant_id = p.id
                    WHERE w.challenge_id = %(challenge_id)s
                    GROUP BY p.first_name, p.last_name, p.id
                    ORDER BY SUM(w.points_earned) DESC;"""
        results = connectToMySQL(db).query_db(query, {"challenge_id": challenge_id})

        leaderboard = []

        for row in results:
            leaderboard.append(row)

        return results