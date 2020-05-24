import json

with open('jsondb.json','w') as file:
	dic = dict()
	dic['userList'] = dict()
	json.dump(dic,file)