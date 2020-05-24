import pymongo
from pymongo import MongoClient
from werkzeug.security import generate_password_hash
from datetime import datetime
from user import *

#conection route----->>>mongodb+srv://abhiraj:navigus@cluster0-rc6jx.mongodb.net/test?retryWrites=true&w=majority


cluster=MongoClient("mongodb+srv://test:testpass@presence-7n1qf.mongodb.net/test?retryWrites=true&w=majority")

db=cluster["navigus"]
collection=db["testdb"]


def login(userid):
	collection.update_one({"user":userid},{"$set":{"loggedin":True, "lastLogged":str(datetime.now())}})
	return


def logout(userid):
	collection.update_one({"user":userid},{"$set":{"loggedin":False, "lastLogged":str(datetime.now())}})
	return

def registerUser(userid,passkey,filename):
	print("Register ",end='')
	print(userid,passkey,filename)
	result = collection.find({"user":userid})
	print("result count",result.count())
	if result.count() == 0:
		collection.insert_one({"user":userid,"pass":generate_password_hash(passkey),"loggedin":False,"lastLogged":str(datetime.now()),"avatar":filename})
		print("Success!")
		return True
	else:
		print("Failed! Username already taken.")
		for i in result:
			print(i["user"])
	return False

def getOnline():
	result = collection.find({"loggedin":True})
	return result

def userLookup(userid):
	user_data = collection.find_one({"user":userid})
	return User(user_data['user'],user_data['pass'],user_data['avatar']) if user_data else None
