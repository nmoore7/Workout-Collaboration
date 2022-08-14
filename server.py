from flask_app import app
from flask_app.controllers import participants
from flask_app.controllers import challenges
from flask_app.controllers import workouts

if __name__ == "__main__":
    app.run(debug=True)