from pymongo import MongoClient,errors

def openMDB(ip,dbName):
	try:
		conn=MongoClient(ip,27017)
		db=conn[dbName]
		return db
	except errors.ConnectionFailure, e:
		return None
