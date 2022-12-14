import pymongo
client = pymongo.MongoClient("mongodb://localhost:27017/")
print (client)
db = client["bikedb"]
items = db["rog_joma"]
for x in items.find():
    print(x)