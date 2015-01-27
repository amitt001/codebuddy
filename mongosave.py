import pymongo
from datetime import datetime

class mongosave:
	currdate = None
	currtime = None
	connection = None
	db = None
	collection = None

	def __init__(self):
		self.connection = pymongo.Connection()
		self.db = self.connection['pastepad_db']
		self.collection = self.db['paste_collection']

	def save(self, _id, data):
		currdate = datetime.now().strftime('%Y-%m-%d')
		currtime = datetime.now().strftime('%H:%M')
		self.collection.insert({'_id': _id, 'paste_doc': data, "date": currdate, 'time': currtime})
		print(list(self.collection.find()))

	def check(self, _id):
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
		