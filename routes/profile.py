# -*- coding: utf-8 -*-
import os, sys, pprint

sys.path.append(os.path.abspath(os.getcwd()))

from flask import Blueprint, jsonify
from flask.globals import request
from routes.auth import login_required
from enviroment.enviroment import db
from utils.gets import get_user
from utils.login_manager import LoginManager

profile = Blueprint("profile", __name__, url_prefix="/profile")

@profile.route("/get_profile", methods=["GET"])
@login_required
def get_profile():
  try:
    user_local = get_user()
    user_db = db.collection_users.find_one({'email': user_local['email']})
    
    if not user_db:
      return jsonify({'message': 'token inválido!'}), 401

    del user_db['password']
    user_db['_id'] = str(user_db['_id'])
    
    return {**user_db}, 200
  except Exception as e:
    return not_found(e)


@profile.route("/update", methods=["POST"])
@login_required
def profile_update():
  try:
    payload = request.get_json()
    user_local = get_user()
    user_db = db.collection_users.find_one({'email': user_local['email']})
    
    if not user_db:
      return jsonify({'message': 'token inválido!'}), 401

    user_merge = {**user_db, **payload}
    db.collection_users.update_one({'email':user_local['email']}, {'$set': user_merge})

    del user_merge['password']
    user_merge['_id'] = str(user_merge['_id'])

    return {**user_merge}, 200
  except Exception as e:
    return not_found(e)


@profile.errorhandler(500)
def not_found(e=None):
  return {'message': 'Error %s' % repr(e), 'status': 500}, 500