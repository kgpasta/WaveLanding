import os
from flask import Flask, render_template, request, abort, make_response
from flask.ext.pymongo import PyMongo
from flask.ext.httpauth import HTTPBasicAuth
from tools import jsonify

app = Flask(__name__)

auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == 'wave':
        return 'ridethewave'
    return None

@auth.error_handler
def unauthorized():
    return make_response(jsonify( { 'error': 'Unauthorized access' } ), 401)

MONGO_URL = os.environ.get('MONGOHQ_URL')

if MONGO_URL:
	app.config['MONGO_URI'] = MONGO_URL

mongo = PyMongo(app,config_prefix='MONGO')

@app.route('/',methods=['GET', 'POST'])
def index():
    return render_template('security.html')
	
@app.route('/home', methods=['GET', 'POST'])
def home():
	print(request.method)
	if request.form['username'] == 'wave' and request.form['password'] == 'ridethewave':
		return render_template('index.html')
	else:
		return render_template('security.html')

@app.route('/wave/workouts', methods = ['GET'])
@auth.login_required
def get_workouts():
    workoutList = []
    for workout in mongo.db.workouts.find():
        workoutList.append(workout)
    
    return jsonify({'workouts':workoutList})

@app.route('/wave/workouts/<ObjectId:workout_id>', methods = ['GET'])
@auth.login_required
def get_workout(workout_id):
    workout = mongo.db.workouts.find_one_or_404(workout_id)
    return jsonify( workout )

@app.route('/wave/workouts', methods = ['POST'])
@auth.login_required
def create_workout():
    if not request.form or not 'title' in request.form:
        abort(400)
    workout = {
        'title': request.form['title'],
        'user': request.form['user'],
        'strokes': request.form['strokes'],
        'lengths': request.form['lengths'],
        'calories': request.form['calories'],
        'raw': request.form['raw']
    }
    mongo.db.workouts.insert(workout)
    return jsonify( { 'workouts': workout } ), 201

@app.route('/wave/workouts/<ObjectId:workout_id>', methods = ['DELETE'])
@auth.login_required
def delete_workout(workout_id):
    workout = mongo.db.workouts.find_one_or_404(workout_id)
    mongo.db.workouts.remove(workout)
    return jsonify( { 'result': True } )

if __name__ == '__main__':
    app.run()
