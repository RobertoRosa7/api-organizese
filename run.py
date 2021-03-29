# -*- coding: utf-8 -*-
import os, sys, time

sys.path.append(os.path.abspath(os.getcwd()))

from flask import Flask, jsonify, request
# from flask_script import Manager, Server
# from flask_pymongo import PyMongo
# from bson.json_util import dumps
from utils.gets import set_user
from pprint import pprint

# from bson.objectid import ObjectId
# from werkzeug.security import check_password_hash, generate_password_hash

from routes.home import home
from routes.dashboard import dashboard
from routes.login import my_login
from routes.profile import profile
from routes.files import files


app = Flask(__name__)
# app.secret_key = 'secretkey'
# app.config['MONGO_URI'] = 'mongodb://localhost:27017/primeiroapp'


app.register_blueprint(my_login)
app.register_blueprint(home)
app.register_blueprint(dashboard)
app.register_blueprint(profile)
app.register_blueprint(files)


@app.route("/", methods=["GET"])
def health_check():
  try:
    return jsonify({'API':"it's working"}), 200
  except Exception as e:
    return jsonify({'message': ''})


@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    # response.headers.add('Access-Control-Allow-Headers', 'Access-Control-Allow-Origin,Access-Control-Allow-Headers,Content-Type,Authorization,Token,Avista-Token,X-Requested-With')
    response.headers.add("Access-Control-Allow-Headers", "Authorization, responseType, Token, Access-Control-Allow-Headers, Origin, Accept, X-Requested-With, Content-Type, Access-Control-Request-Method, Access-Control-Request-Headers");
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE')
    # response.headers.add('Access-Control-Allow-Credentials', 'true')
    content_type = response.headers['content-type']
    
    if content_type == 'application/octet-stream':
      return request.data

    # if content_type == 'application/json':
    #     request_json = request.get_json(silent=True)
    #     if request_json and 'name' in request_json:
    #         name = request_json['name']
    #     else:
    #         raise ValueError("JSON is invalid, or missing a 'name' property")
    # elif content_type == 'application/octet-stream':
    #     name = request.data
    # elif content_type == 'text/plain':
    #     name = request.data
    # elif content_type == 'application/x-www-form-urlencoded':
    #     name = request.form.get('name')
    # else:
    #     raise ValueError("Unknown content type: {}".format(content_type))
    # return 'Hello {}!'.format(escape(name))

    return response


if __name__ == "__main__":
  app.run(debug=True)