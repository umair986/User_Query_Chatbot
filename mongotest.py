from pymongo import MongoClient
client = MongoClient("")
print(client.list_database_names())
