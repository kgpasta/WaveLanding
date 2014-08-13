import os
from flask import Flask, render_template, request, abort, make_response
from flask.ext.pymongo import PyMongo
from tools import jsonify

app = Flask(__name__)

mongo = PyMongo(app)

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
def get_workouts():
    workoutList = []
    for workout in mongo.db.workouts.find():
        workoutList.append(workout)
    
    return jsonify({'workouts':workoutList})

@app.route('/wave/workouts/<ObjectId:workout_id>', methods = ['GET'])
def get_workout(workout_id):
    workout = mongo.db.workouts.find_one_or_404(workout_id)
    return jsonify( workout )

@app.route('/wave/workouts', methods = ['POST'])
def create_workout():
    if not request.form or not 'title' in request.form:
        abort(400)
    workout = {
        'title': request.form['title'],
        'strokes': request.form['strokes'],
        'lengths': request.form['lengths'],
        'calories': request.form['calories']
    }
    mongo.db.workouts.insert(workout)
    return jsonify( { 'workouts': workout } ), 201

@app.route('/wave/workouts/<ObjectId:workout_id>', methods = ['DELETE'])
def delete_workout(workout_id):
    workout = mongo.db.workouts.find_one_or_404(workout_id)
    mongo.db.workouts.remove(workout)
    return jsonify( { 'result': True } )

if __name__ == '__main__':
    app.run(debug = True)
