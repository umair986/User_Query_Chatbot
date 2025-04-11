from pymongo import MongoClient
client = MongoClient("mongodb+srv://mohumair1901:mohumair1901@cluster0.r4h0l.mongodb.net/")
print(client.list_database_names())
