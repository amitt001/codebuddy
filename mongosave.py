'''
Use this code while running the webapp on localhost 
with a mongodb sever running
'''

import pymongo
from bson.objectid import ObjectId
from datetime import datetime

class mongosave:
	currdate = None
	currtime = None
	connection = None
	db = None
	collection = None

	def __init__(self):
		self.connection = pymongo.Connection()
		self.db = self.connection['codebuddy_db']
		#self.collection = self.db['paste_collection']

	def userlogin(self, email, password):
		#self.collection = self.db['user_login']
		self.collection = self.db['codebuddy_collect']
		try:
			result = list(self.collection.find({'user_email': email}))
			if not len(result):
				print('########new######')
				result = str(self.collection.insert({'user_email': email, 'user_password': password}))
			else:
				if result[0].get('user_password') == password:
					result = str(result[0].get('_id'))
					print("$$$$$$$$$$$$$$$$$$$$$$$$$$$$$")
					print('####already#####', result)
				else:
					print('####already#####')
					return -2

			return result

		except Exception, e:
			print(e)			
			return -1

	def login_check(self, _id):
		self.collection = self.db['codebuddy_collect']
		result = list(self.collection.find({'_id': ObjectId(_id)}))
		print str(result[0].get('_id'))
		if str(result[0].get('_id')) == _id:
			return 1
		else: 
			return -1


	def save(self, _id, data):
		self.collection = self.db['paste_collection']
		currdate = datetime.now().strftime('%Y-%m-%d')
		currtime = datetime.now().strftime('%H:%M')
		self.collection.insert({'_id': _id, 'paste_doc': data, "date": currdate, 'time': currtime})
		print(list(self.collection.find()))

	def check(self, _id):
		self.collection = self.db['paste_collection']
		try:
			result = list(self.collection.find({'_id': _id}, {'paste_doc':1, '_id':0}))
			if not len(result):
				print 'returning coz no data'
				return None

			restext = result[-1].get('paste_doc', None)
			print restext
			return restext
		except Exception, e:
			print e
		
