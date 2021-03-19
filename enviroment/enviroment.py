import os, sys

sys.path.append(os.path.abspath(os.getcwd()))

from pymongo import MongoClient

# API = 'http://localhost:4200' # frontend api

API = 'https://robertorosa7.github.io/web-organizese'
# API = 'https://api-organizese.000webhostapp.com'

PRIMEIROAPP_API_DEV = os.environ.get('PRIMEIROAPP_API_DEV')
PRIMEIROAPP_API_PROD = os.environ.get('PRIMEIROAPP_API_PROD')

# conn = MongoClient(host=PRIMEIROAPP_API_DEV, port=27017)
conn = MongoClient(host=PRIMEIROAPP_API_PROD, port=27017)

# db = client.test
# print(client.list_database_names())

db = conn['primeiroapp']