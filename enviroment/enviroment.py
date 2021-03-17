import os, sys

sys.path.append(os.path.abspath(os.getcwd()))

from pymongo import MongoClient

API = 'http://localhost:4200' # frontend api

PRIMEIROAPP_API_DEV = os.environ.get('PRIMEIROAPP_API_DEV')
PRIMEIROAPP_API_PROD = os.environ.get('PRIMEIROAPP_API_PROD')

# conn = MongoClient(host=PRIMEIROAPP_API_DEV, port=27017)
conn = MongoClient(host=PRIMEIROAPP_API_PROD, port=27017)

# client = MongoClient("mongodb+srv://beto:beto1234@cluster0.rt58f.mongodb.net/primeiroapp?retryWrites=true&w=majority")
# client = MongoClient("mongodb://beto:beto123@cluster0-shard-00-00.rt58f.mongodb.net:27017,cluster0-shard-00-01.rt58f.mongodb.net:27017,cluster0-shard-00-02.rt58f.mongodb.net:27017/myFirstDatabase?ssl=true&replicaSet=atlas-xu6lpq-shard-0&authSource=admin&retryWrites=true&w=majority")
# db = client.test
# print(client.list_database_names())

db = conn['primeiroapp']