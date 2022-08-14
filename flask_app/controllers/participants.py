from flask import render_template, session, redirect, request
from crypt import methods
from flask_app import app
from flask_app.models.participant import Participant
from flask import flash
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def login_page():
    return render_template('login.html')

@app.route('/sign_up', methods=['POST'])
def register():
    if not Participant.login_validation(request.form):
        return redirect('/')
    data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = Participant.save(data)
    session['participant_id'] = id
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    participant = Participant.get_by_email(request.form)
    if not participant:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(participant.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['participant_id'] = participant.id
    return redirect('/challenges')

@app.route('/view_participant/<int:participant_id>')
def view_participant(participant_id):
    data = {"participant_id" : participant_id}
    return render_template('view_participant.html', participant=Participant.get_by_id(data))