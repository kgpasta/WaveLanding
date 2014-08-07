import os
from flask import Flask, render_template, request, jsonify, abort, make_response

app = Flask(__name__)

workouts = [
    {
        'id': 1,
        'title': 'Workout 1',
        'strokes': 250, 
        'lengths': 10,
        'calories': 300,
    },
    {
        'id': 2,
        'title': 'Workout 2',
        'strokes': 150, 
        'lengths': 6,
        'calories': 150,
    },
]

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
    return jsonify( { 'workouts': workouts } )

@app.route('/wave/workouts/<int:workout_id>', methods = ['GET'])
def get_workout(workout_id):
    workout = filter(lambda t: t['id'] == workout_id, workouts)
    if len(workout) == 0:
        abort(404)
    return jsonify( { 'workout': workout[0] } )

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

@app.route('/wave/workouts', methods = ['POST'])
def create_workout():
    print(request.json)
    if not request.json or not 'title' in request.json:
        abort(400)
    workout = {
        'id': workouts[-1]['id'] + 1,
        'title': request.json['title'],
        'strokes': request.json['strokes'],
        'lengths': request.json['lengths'],
        'calories': request.json['calories']
    }
    workouts.append(workout)
    return jsonify( { 'workouts': workout } ), 201

@app.route('/wave/workouts/<int:task_id>', methods = ['DELETE'])
def delete_workout(workout_id):
    workout = filter(lambda t: t['id'] == workout_id, workouts)
    if len(workout) == 0:
        abort(404)
    workouts.remove(workout[0])
    return jsonify( { 'result': True } )

if __name__ == '__main__':
    app.run(debug = True)
