'''
This code conneccts with https://mongolab.com/ api

saves the deployed heroku apps data in mongodb 

For localhost code see mongosave.py

'''


import pymongo
import json
import requests
from bson.objectid import ObjectId
from datetime import datetime

class mongosave:
	currdate = None
	currtime = None
	connection = None
	db = None
	collection = None

	def __init__(self):
            requests.packages.urllib3.disable_warnings()

		#self.connection = pymongo.Connection()
		#self.db = self.connection['codebuddy_db']
                #res = requests.get('https://api.mongolab.com/api/1/databases?apiKey=xxxxxxxxxxx')
                #print res.text
		#self.collection = self.db['paste_collection']

	def userlogin(self, email, password):
		#self.collection = self.db['user_login']
		#self.collection = self.db['codebuddy_collect']
                data = {'user_email': email, 'user_password': password}
                headers = {'content-type': 'application/json'}

		try:
			#result = list(self.collection.find({'user_email': email}))
                        geturl = 'https://api.mongolab.com/api/1/databases/codebuddy_db/collections/codebuddy_collect?q={"user_email": "%s"}&apiKey=xxx' % (email)
                        response = requests.get(geturl)
                        result = response.json()
                        print 'RESULT', result
			if not len(result):
				print('########new######')
				#result = str(self.collection.insert({'user_email': email, 'user_password': password}))
                                response  = requests.post('https://api.mongolab.com/api/1/databases/codebuddy_db/collections/codebuddy_collect?apiKey=xxxx', data=json.dumps(data), headers=headers)
                                result = response.json()
                                result = str(result.get('_id').get('$oid'))
			else:
				if result[0].get('user_password') == password:
					#result = str(result[0].get('_id'))
                                        result = str(result[0].get('_id').get('$oid'))
					print('####already#####', result)
				else:
					print('####already#####')
					return -2

			return result

		except Exception, e:
			print(e)			
			return -1

	def login_check(self, _id):
		#self.collection = self.db['codebuddy_collect']
		#result = list(self.collection.find({'_id': ObjectId(_id)}))
                geturl= 'https://api.mongolab.com/api/1/databases/codebuddy_db/collections/codebuddy_collect?q={"_id": {"$oid": "%s"}}&apiKey=xxxx'% (_id)
                response = requests.get(geturl)
                result = response.json()
                try:
                    if str(result[0].get('_id').get('$oid')) == _id:
        		return 1
    		    else:
                        print 'HERERERER'
		        return -1
                except KeyError, e:
                    print "HERE", e
                    return -1


	def save(self, _id, data):
		#self.collection = self.db['paste_collection']
		currdate = datetime.now().strftime('%Y-%m-%d')
		currtime = datetime.now().strftime('%H:%M')
                data = {'_id': _id, 'paste_doc': data, 'date': currdate, 'time': currtime}
                headers = {'content-type': 'application/json'}

                response  = requests.post('https://api.mongolab.com/api/1/databases/codebuddy_db/collections/paste_collection?apiKey=xxxxxxxxx', data=json.dumps(data), headers=headers)
                result = response.json()
		#self.collection.insert({'_id': _id, 'paste_doc': data, "date": currdate, 'time': currtime})
		#print(list(self.collection.find()))

	def check(self, _id):
		#self.collection = self.db['paste_collection']
		try:
                        geturl= 'https://api.mongolab.com/api/1/databases/codebuddy_db/collections/paste_collection?q={"_id": "%s"}&apiKey=xxxx'% (_id)
                        response = requests.get(geturl)
                        result = response.json()
			#result = list(self.collection.find({'_id': _id}, {'paste_doc':1, '_id':0})) 
			if not len(result):
				print 'returning coz no data'
				return None

			restext = result[-1].get('paste_doc', None)
			return restext
		except Exception, e:
			print e
		
