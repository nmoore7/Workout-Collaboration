from flask import render_template, session, redirect, request, url_for, send_from_directory
from flask_app import app
from flask_app.models.participant import Participant
from flask_app.models.challenge import Challenge
from flask_app.models.workout import Workout
from flask import flash
import os
from werkzeug.utils import secure_filename


DOWNLOAD_FOLDER = "static/img/uploads"
UPLOAD_FOLDER = "/Users/nathanielmoore/Documents/CodingDojo/projects_algos/personal_project/workout_collaboration/flask_app/static/img/uploads"
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'heic'}

IMG_FOLDER = os.path.join('static', 'IMG')

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

app.config['DOWNLOAD_FOLDER'] = DOWNLOAD_FOLDER

@app.route('/log_workout')
def log_workout():
    challenge_id = session['challenge_id']
    return render_template('new_workout.html', participant = Workout.get_participants_in_challenge(challenge_id))

def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/save_workout', methods = ['GET', 'POST'])
def upload_file():

    if not Workout.workout_validate(request.form):
        return redirect('/log_workout')
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            Workout.save_workout(request.form, filename)
            Workout.associate_participants_and_workouts(session['participant_id'], Workout.get_latest_workout())
            return redirect('/view_workouts')

    return redirect('/log_workout')

@app.route('/view_workouts')
def view_workouts():
    Flask_Logo = os.path.join(app.config['DOWNLOAD_FOLDER'])
    return render_template('participant_workouts.html', workout = Workout.get_all_in_challenges(session['challenge_id']), user_image = app.config['DOWNLOAD_FOLDER'])

@app.route('/uploads/<name>')
def download_file(name):
    return send_from_directory(app.config["UPLOAD_FOLDER"], name)
