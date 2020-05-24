import json
from werkzeug.security import generate_password_hash
from user import *
from datetime import datetime


class JSONModule:

	def __init__(self):
		self.lock = False

	def getdata(self):
		return json.load(open('jsondb.json','r'))

	def setdata(self,data):
		json.dump(data,open('jsondb.json','w'))

	def getLogged(self,userid):
		data = self.getdata()
		return data['userList'][userid]['loggedin']

	def login(self,userid):
		while self.lock:
			pass
		self.lock = True
		data = self.getdata()
		data['userList'][userid]['loggedin'] = True
		data['userList'][userid]['lastLogged'] = str(datetime.now())
		self.setdata(data)
		self.lock = False

	def logout(self,userid):
		while self.lock:
			pass
		self.lock = True
		data = self.getdata()
		data['userList'][userid]['loggedin'] = False
		data['userList'][userid]['lastLogged'] = str(datetime.now())
		self.setdata(data)
		self.lock = False

	def registerUser(self,userid,passkey,filename):
		while self.lock:
			pass
		self.lock = True
		data = self.getdata()

		if userid not in data['userList'].keys():
			data['userList'][userid] = {"user":userid,"pass":generate_password_hash(passkey),"avatar":filename,"loggedin":False,"lastLogged":str(datetime.now())}
			self.setdata(data)
			self.lock = False
			return True
		else:
			print("Failed! Username already taken.")
			self.lock = False
			return False

	def getOnline(self):
		data = self.getdata()
		result = list()
		for user in data['userList'].keys():
			if data['userList'][user]['loggedin']:
				result.append(data['userList'][user])
		return result

	def userLookup(self,userid):
		data = self.getdata()
		if userid not in data['userList'].keys():
			return None
		result = data['userList'][userid]
		return User(result['user'],result['pass'],result['avatar'])