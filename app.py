from flask import Flask, flash, request, render_template, jsonify, redirect, url_for, session
import data
import os
from werkzeug.utils import secure_filename
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from user import *
import jsonmodule
from flask_socketio import SocketIO, join_room
from flask_cors import CORS
from datetime import timedelta

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)
app.config['UPLOAD_FOLDER'] = 'static/images'
app.secret_key = os.urandom(24)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.refresh_view = 'login'
login_manager.needs_refresh_message = u'Session timed out. You need to re-login.'
login_manager.needs_refresh_category = 'info'

jsonmod = jsonmodule.JSONModule()


login_manager.init_app(app)

@app.before_request
def before_request():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(minutes=5)

@app.route('/reading')
@login_required
def reading():
	onlinePeople = data.getOnline()
	return render_template('readPage.html', data=onlinePeople)

@app.route('/', methods=['GET'])
def index():
	if current_user.is_authenticated:
		return redirect(url_for('reading'))
	#INDEX PAGE
	params = 'Landing Page'
	if request.method == 'GET':
		return render_template('index.html',params=params)
	return render_template('index.html',params=params)

@app.route('/register', methods=['POST','GET'])
def register():
	if current_user.is_authenticated:
		return redirect(url_for('reading'))
	message = ''
	if request.method == 'POST':
		user_id = request.form.get('userid')
		passkey = request.form.get('pass')
		file = request.files['file']

		if file.filename == '':
			message = 'Please select an image'
			return render_template('index.html',message=message)
		if file:
			message = 'Error in registering user.'
			filename = secure_filename(file.filename)
			file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
		if data.registerUser(user_id,passkey,filename):
			message = 'User registered successfully! Login with the details.'
		else:
			message = 'Username already exists'
	return render_template('index.html',message=message)

@login_manager.user_loader
def load_user(userid):
	return data.userLookup(userid)

@app.route('/login', methods=['GET','POST'])
def login():
	if current_user.is_authenticated:
		return redirect(url_for('reading'))
	message = ''
	if request.method == 'POST':
		user_id = request.form.get('userid')
		passkey = request.form.get('pass')
		user = data.userLookup(user_id)

		if user and user.check_password(passkey):
			# if jsonmod.getLogged(user_id) == False:
			login_user(user)
			data.login(user.userid)
			return redirect(url_for('reading'))
			# else:
			# 	message = 'User already logged in!'
		else:
			message = 'Login failed! Check username and password.'
	return render_template('index.html',message=message)

@app.route('/logout')
@login_required
def logout():
	data.logout(current_user.userid)
	logout_user()
	userdata = data.getOnline()
	result = list()
	for x in userdata:
		result.append({"userid":x['user'], "avatar":x['avatar'], "lastlogin":str(x['lastLogged'])})
	socketio.emit('join_reading_announcement', {"resultCursor":result})
	return redirect(url_for('index'))

@socketio.on('leave_reading')
def leave_reading_handler(userdata):
	userid = str(userdata['userid'])
	app.logger.info("Left "+userid)
	logout()
	socketio.emit('leave_reading_announcement',{"userid":userid})

@socketio.on('join_reading')
def join_reading_handler(userdata):
	app.logger.info("Joined "+str(userdata['userid']))
	join_room('file1')
	userdata = data.getOnline()
	result = list()
	for x in userdata:
		result.append({"userid":x['user'], "avatar":x['avatar'], "lastlogin":str(x['lastLogged'])})
	socketio.emit('join_reading_announcement', {"resultCursor":result})

if __name__ == '__main__':
	socketio.run(app, debug=True)