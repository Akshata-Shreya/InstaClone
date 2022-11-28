from pymongo import MongoClient
import json 

file = open('config.json')
config_json = json.load(file)
file.close()

client = MongoClient(config_json["MongoClient"], connect=False)
db_handle = client['Instagram']
user_handle = db_handle['user']
post_handle = db_handle['post']
