from pymongo import MongoClient

client = MongoClient('mongodb+srv://igdbuser:igdbuser@cluster0.xztfj.mongodb.net/Instagram?retryWrites=true&w=majority', connect=False)
db_handle = client['Instagram']
user_handle = db_handle['user']
