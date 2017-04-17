#coding:UTF-8
import pymongo
from pymongo import MongoClient

client = MongoClient()
db=client.myDB
db.myCol.drop()
db.myCol.insert_one(
   {"Persons":[{"id":"405", "이름":"js1"},{"id":"406", "이름":"js2"}]}
)
results = db.myCol.find()
for r in results:
        print r['Persons']