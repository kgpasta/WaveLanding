import os
from flask import Flask, render_template, request

app = Flask(__name__)

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

if __name__ == '__main__':
    app.run()
