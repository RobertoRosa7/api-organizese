import os, sys
from typing import Text

sys.path.append(os.path.abspath(os.getcwd()))

from pymongo import MongoClient

# API = 'http://localhost:4200' # frontend api
# API = 'https://robertorosa7.github.io/web-organizese'

API = 'https://api-organizese.000webhostapp.com'
MODE = os.environ.get('PRIMEIROAPP_API_PROD')
TEXT = ''
PRIMEIROAPP_API_DEV = os.environ.get('PRIMEIROAPP_API_DEV')
PRIMEIROAPP_API_PROD = os.environ.get('PRIMEIROAPP_API_PROD')

# conn = MongoClient(host=PRIMEIROAPP_API_DEV, port=27017)
# conn = MongoClient(host=PRIMEIROAPP_API_PROD, port=27017)

for i in sys.argv:
  if i == 'dev':
    MODE = PRIMEIROAPP_API_DEV
    API = 'http://localhost:4200'
    TEXT = 'DEV'
  else:
    MODE = PRIMEIROAPP_API_PROD
    API = 'https://api-organizese.000webhostapp.com'
    TEXT = 'PROD'
  
conn = MongoClient(host=MODE, port=27017)
db = conn['primeiroapp']
print('The API is running in: {0} mode'.format(TEXT))